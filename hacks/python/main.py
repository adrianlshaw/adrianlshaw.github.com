from js import document
import asyncio

# The following is only needed for the graph
import matplotlib.pyplot as plt
import numpy as np
from pyscript import display

input = Element("in").element
output = Element("out").element

# This is the main callback, but we don't want to block
# the browser so we kickstart an async function call
def on_input(*args):
    #print("hello")
    output.innerHTML = ""
    document.body.classList.add("wait")
    input.classList.add("wait")

    asyncio.create_task(on_input_catch_all(args))

async def on_input_catch_all(*args):
    input.classList.remove("invalid")

    if input.value:
        try:
            await on_input_unwrapped(*args)
        except Exception as e:
            input.classList.add("invalid")
            output.innerHTML = f'<span class="color-warning">{str(e)}</span>'

    document.body.classList.remove("wait")
    input.classList.remove("wait")

async def on_input_unwrapped(*args):
    output.innerHTML = "You typed " + str(input.value)
    #print("You typed " + str(input.value))
    await show_graph()


async def show_graph():
    mpl = Element("mpl").element
    mpl.innerHTML = ""
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    display(fig, target="mpl")
