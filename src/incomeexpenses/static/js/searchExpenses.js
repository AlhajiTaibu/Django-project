const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector('.table-output')
const appTable = document.querySelector('.app-table')
const tableBody = document.querySelector('.table-body')
const paginatorContainer = document.querySelector('.paginator-container')
tableOutput.style.display="none";

searchField.addEventListener('keyup', (e)=>{
    const searchValue= e.target.value;
    if(searchValue.trim().length>0){
        paginatorContainer.style.display='none'
        tableBody.innerHTML =''
        fetch('/search-expenses',{
            body: JSON.stringify({searchText:searchValue}),
            method: "POST",
      }).then(res=>res.json()).then((data)=>{
        console.log('data', data);
        appTable.style.display = 'none'
        tableOutput.style.display = "block"
        if(data.length==0){
        tableOutput.innerHTML= "No result found"
        paginatorContainer.style.display='none'
        }else{
            data.forEach(item=>{
             tableBody.innerHTML+=
          '<tr><td>'+
          item.id+'</td><td>'
          +item.description+'</td><td>'
          +item.amount+'</td><td>'
          +item.category+'</td><td>'
          +item.date+'</td><td><button class="btn btn-secondary">Edit</button></td><td><button class="btn btn-danger">Delete</button></td></tr>'
            })

        }
    })
    }else{
        appTable.style.display = 'block'
        paginatorContainer.style.display = 'block'
        tableOutput.style.display = 'none'
    }
})