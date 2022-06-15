const checkForError = response => {
    if (!response.ok) throw Error(response.statusText);
    return response.json();
};

export const get = (URL) => {
    fetch(URL)
        .then(checkForError)
        .then(data => console.log("data", data))
        .catch(error => {
            console.log("error", error);
        });
}
