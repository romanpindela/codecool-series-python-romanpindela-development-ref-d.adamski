const disable = (...args) => args.forEach(arg => arg.disabled = true)

const unable = (...args) => args.forEach(arg => arg.disabled = false)

const clearValue = (...args) => args.forEach(arg => arg.value = "")

const clearTextContent = (...args) => args.forEach(arg => arg.textContent = "")

const clearInnerHtml = (...args) => args.forEach(arg => arg.innerHTML = "")

const setDisplay = (display, ...elements) => elements.forEach(el => el.style.display = display)

export {disable, unable, clearValue, clearTextContent, clearInnerHtml, setDisplay}