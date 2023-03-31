import asyncio
from asyncio import Future

import grpc
from grpc._cython import cygrpc
from grpc._channel import _handle_event, _EMPTY_FLAGS


class FutureWrapper:
    """
    Wraps a grpc future function to produce an async function.
    Example Usage:
    ```
    async_rpc = FutureWrapper(stub.RpcCall)
    ...
    value = await async_rpc(request)
    ```
    """

    # Inspired by https://github.com/grpc/grpc/issues/6046#issuecomment-319547191
    def __init__(self, func, loop=None):
        self.func = func
        self.loop = asyncio.get_event_loop() if loop is None else loop

    def _fwrap(self, future, grpc_future):
        try:
            future.set_result(grpc_future.result())
        except Exception as e:
            future.set_exception(e)

    def __call__(self, req):
        """
        Get an asyncio.Future associated with a grpc call.
        """
        # Step 1: Initiate request, and get a grpc.Future that will be "triggered"
        # when the rpc call comes back (or errors)
        grpc_future = self.func.future(req)
        # Step 2: make a new asyncio Future, which we can return.
        future = asyncio.Future()
        # Step 3: hook them together. Add a callback to the grpc.Future so that when it
        # triggers, it alerts the main asyncio loop that its ready, and then when the
        # asyncio loop is ready ("soon"), the asyncio future is passed the result from
        # the grpc.Future. (Or passed the exception, if one of those happened.)
        grpc_future.add_done_callback(
            lambda _: self.loop.call_soon_threadsafe(self._fwrap, future, grpc_future)
        )
        return future


class AsyncStream:
    """
    A grpc stream wrapper that can be iterated over asynchronously.
    ```
    async for response in AsyncStream(stub.RpcCall(request)):
        print(response)
    ```
    """

    # Inspired by https://github.com/grpc/grpc/issues/7910#issuecomment-243290904

    def __init__(self, stream, loop=None):
        self.stream = stream
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    def handle_event(self, event, future):
        """
        Event handler called by grpc when a message is received
        (or any other event)
        """
        with self.stream._state.condition:
            callbacks = _handle_event(event, self.stream._state,
                                      self.stream._response_deserializer)
            self.stream._state.condition.notify_all()
            done = not self.stream._state.due
            self._process_future(future)  # this is the key patch point
        for callback in callbacks:
            callback()
        return self.stream._call if done else None

    def _process_future(self, future):
        # The grpc callback triggered; time to figure out what happened,
        # and set the given future if necessary.
        if self.stream._state.response is not None:
            # event: we received something
            # Put it in the future and move on
            response = self.stream._state.response
            self.stream._state.response = None
            self.loop.call_soon_threadsafe(future.set_result, response)
            return
        elif cygrpc.OperationType.receive_message not in self.stream._state.due:
            if self.stream._state.code is grpc.StatusCode.OK:
                # event: stream closed
                # Tell the future we're done
                self.loop.call_soon_threadsafe(future.set_exception,
                                               StopAsyncIteration())
                return
            elif self.stream._state.code is not None:
                # event: some sort of stream error
                # self.stream is a grpc._Rendezvous object that normally
                # gives us stream results, but they double as grpc.RpcError
                # So we raise it
                self.loop.call_soon_threadsafe(future.set_exception,
                                               self.stream)
                return

        # An event we aren't interested in happened; we should wait for the next event.
        #########
        event_handler = lambda event: self.handle_event(event, future)
        self.stream._call.start_client_batch(
            (cygrpc.ReceiveMessageOperation(_EMPTY_FLAGS), ), event_handler)
        self.stream._state.due.add(cygrpc.OperationType.receive_message)

    # Similar to first part of grpc._channel._Rendevous._next
    def _next(self):
        """
        Returns a future for the next value in an iterator
        """
        # ensure there is only one outstanding request at any given time, or segfault happens
        if cygrpc.OperationType.receive_message in self.stream._state.due:
            raise ValueError("Prior future was not resolved")

        future = Future()
        # this method is the same as the first part of _Rendevous._next
        with self.stream._state.condition:
            if self.stream._state.code is None:
                # Give grpc an event handler (self.handle_event) to call
                # whenever something changes with the stream
                # e.g. a batch is received or the channel is closed
                event_handler = lambda event: self.handle_event(event, future)
                self.stream._call.start_client_batch(
                    (cygrpc.ReceiveMessageOperation(_EMPTY_FLAGS), ),
                    event_handler)
                self.stream._state.due.add(
                    cygrpc.OperationType.receive_message)
            # if the stream is already finished (OK), just end now
            elif self.stream._state.code is grpc.StatusCode.OK:
                future.set_exception(StopAsyncIteration())
            # if there's already an error in the stream, set the error and return
            else:
                future.set_exception(self.stream)
        return future

    def __aiter__(self):
        return self

    async def __anext__(self):
        value = await self._next()
        return value


class AsyncStreamer:
    def __init__(self, func):
        self.func = func

    def __call__(self, req):
        stream = self.func(req)
        return AsyncStream(stream)