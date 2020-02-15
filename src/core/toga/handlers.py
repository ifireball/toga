try:
    import asyncio
except ImportError:
    asyncio = None
import inspect
import sys
import traceback


async def long_running_task(generator, cleanup):
    """Run a generator as an asynchronous coroutine

    """
    try:
        while True:
            delay = next(generator)
            await asyncio.sleep(delay)
    except StopIteration:
        if cleanup:
            cleanup()
    except Exception as e:
        print('Error in long running handler:', e, file=sys.stderr)
        traceback.print_exc()


async def handler_with_cleanup(handler, cleanup, interface, *args, **kwargs):
    try:
        await handler(interface, *args, **kwargs)
        if cleanup:
            cleanup()
    except Exception as e:
        print('Error in async handler:', e, file=sys.stderr)
        traceback.print_exc()


def wrapped_handler(interface, handler, cleanup=None):
    """Wrap a handler provided by the user so it can be invoked.

    If the handler is a bound method, or function, invoke it as it,
        and return the result.
    If the handler is a generator, invoke it asynchronously, with
        the yield values from the generator representing the duration
        to sleep between iterations.
    If the handler is a coroutine, install it on the asynchronous
        event loop.

    Returns a wrapped function that will invoke the handler, using
    the interface as context. The wrapper function is annotated with
    the original handler function on the `_raw` attribute.
    """
    if asyncio is not None:
        # Use asyncio-based implementation on platforms that have it
        return asyncio_wrapped_handler(interface, handler, cleanup)
    # Fallback to a simple and limited implementation
    return synchronous_wrapped_handler(interface, handler, cleanup)

def asyncio_wrapped_handler(interface, handler, cleanup=None):
    if handler:
        def _handler(widget, *args, **kwargs):
            if asyncio.iscoroutinefunction(handler):
                asyncio.ensure_future(
                    handler_with_cleanup(handler, cleanup, interface, *args, **kwargs)
                )
            else:
                result = handler(interface, *args, **kwargs)
                if inspect.isgenerator(result):
                    asyncio.ensure_future(
                        long_running_task(result, cleanup)
                    )
                else:
                    try:
                        if cleanup:
                            cleanup()
                        return result
                    except Exception as e:
                        print('Error in handler:', e, file=sys.stderr)
                        traceback.print_exc()

        _handler._raw = handler

        return _handler

def synchronous_wrapped_handler(interface, handler, cleanup):
    if not handler:
        return
    result = handler(interface, *args, **kwargs)
    if inspect.isgenerator(result):
        raise NotImplementedError(
            "async/generator event callbacks are not supported on this platform"
        )
    try:
        if cleanup:
            cleanup()
        return result
    except Exception as e:
        print('Error in handler:', e, file=sys.stderr)
        traceback.print_exc()
