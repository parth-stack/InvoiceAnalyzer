export function fetchContent(){
    const url = `http://127.0.0.1:5000/api/v1?query=status`
    
    // fetch(url, {
    //     method: "GET"
    // }).then(response => {
    //     return response.json();
    // }).then(result => {
    //     console.log(result)
    //     return result    
    // }).catch(error => {})

    var request = new XMLHttpRequest();
    request.open('GET', url, false);  // `false` makes the request synchronous
    request.send(null);
    
    if (request.status === 200) {
        let obj = JSON.parse(request.responseText)
        console.log(obj)
        return obj
    }

    return 1
}