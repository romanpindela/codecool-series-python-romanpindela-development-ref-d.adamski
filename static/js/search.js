import {fetchApiGet} from "./data_manager.js"
import {clearInnerHtml} from "./utils.js";

const searchInput = document.querySelector("#searchMovie")
const resultDiv = document.querySelector("#searchResult")

searchInput.addEventListener("input", function (e) {
    const dbUrl = `http://127.0.0.1:5000/shows/${e.target.value}`
    fetchApiGet(dbUrl, showSearchResults, clearSearchResults)
})

const showSearchResults = data => {
    clearInnerHtml(resultDiv)
    let resultsList = document.createElement("ul")
    for (let result of data.slice(0, 30)){
        let resultElement = document.createElement("li")
        let resultLink = document.createElement("a")
        resultLink.setAttribute("href", `show/${result.id}`)
        resultLink.textContent = result.title
        resultElement.appendChild(resultLink)
        resultsList.appendChild(resultElement)
    }
    resultDiv.appendChild(resultsList)
}

const clearSearchResults = () => {
    clearInnerHtml(resultDiv)
}