import {fetchApiPost} from "./data_manager.js";

const newActorName = document.querySelector("#actorName")
const actorId = document.querySelector("#actorId")
const submitButton =document.querySelector("#changeActorNameSubmitBtn")

submitButton.addEventListener("click", e => {
    e.preventDefault()
    fetchApiPost(`/edit_actor/${actorId.value}`, changeNameCallback, {
        actor_id: actorId.value,
        actor_name: newActorName.value
    })
})

const changeNameCallback = data => {
    if (data.changed){
        alert("Name changed!")
        window.location.reload()
    }
    else{
        alert("something went wrong")
    }
}