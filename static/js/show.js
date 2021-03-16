import {fetchApiPost} from "./data_manager.js";
import {setDisplay} from "./utils.js";

const showAddSeasonInputsBtn = document.querySelector("#showAddSeasonInputs")
const seasonNumberInput = document.querySelector("#seasonNumber")
const seasonTitleInput = document.querySelector("#seasonTitle")
const seasonOverviewInput = document.querySelector("#seasonOverview")
const addSeasonBtn = document.querySelector("#addSeason")
const seasonNumbers = document.querySelectorAll(".season-number")
const showIdHiddenInput = document.querySelector("#showId")

showAddSeasonInputsBtn.addEventListener("click", e => {
    setDisplay("inline-block", seasonNumberInput, seasonTitleInput, seasonOverviewInput, addSeasonBtn)
    setDisplay("none", e.target)
    seasonNumberInput.value = getLastSeason() + 1
})

addSeasonBtn.addEventListener("click", e => {
    if (checkTitleLength()){
        fetchApiPost("/add_new_season", reloadIfSuccessfullyAddedSeason, {
            show_id: showIdHiddenInput.value,
            season_number: seasonNumberInput.value,
            title: seasonTitleInput.value,
            overview: seasonOverviewInput.value
        })
    }
    else {
        alert("Title is too short!")
    }
})

const getLastSeason = () => {
    let lastSeason = 0
    for (let currentSeason of seasonNumbers) {
        if (parseInt(currentSeason.innerText) > lastSeason)
            lastSeason = parseInt(currentSeason.innerText)
    }
    return lastSeason
}

const checkTitleLength = () => seasonTitleInput.value.length > 5

const reloadIfSuccessfullyAddedSeason = data => {
    if (data.added)
        window.location.reload()
    else
        alert("something went wrong")

}