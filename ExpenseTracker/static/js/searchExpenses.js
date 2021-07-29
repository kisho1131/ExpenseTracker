const searchField = document.querySelector("#search")
const tableOutput = document.querySelector(".table-output")
const appTable = document.querySelector(".app-table")
const pagination = document.querySelector(".pagination-container")
const tableBody = document.querySelector(".tbody")
const noResults = document.querySelector(".no-results")
tableOutput.style.display = "none"

searchField.addEventListener("keyup", (e)=>{
    const searchValue = e.target.value
    tableBody.innerHTML = ""
    if(searchValue.trim().length > 0){
        pagination.style.display ="none"
        console.log('searchvalue', searchValue)

        fetch("/search-expenses", {
            // convert the javascript object into the json object --> seach = id in the index.html
            body:JSON.stringify({search : searchValue}),
            method : "POST",
        }).then(res => res.json()).then((data)=>{
            console.log('data', data)
            appTable.style.display= "none"
            tableOutput.style.display = "block"
            if(data.length === 0){
                noResults.style.display = "block";
                tableOutput.innerHTML = "No Result Found"
            }else{
                data.forEach(item => {
                    noResults.style.display = "none";
                    tableBody.innerHTML += `
                        <tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        </tr>`;
                        
                });
            }
        });
    }else{
        tableOutput.style.display= 'none'
        appTable.style.display="block"
        pagination.style.display= "block"
    }
})