<script >
	import { onMount } from "svelte";

    let loansUrl = "http://127.0.0.1:8000/borrow/1";
    let booksUrl = "http://127.0.0.1:8000/api/books";
    let extendLoansUrl = "";
    let books = [];
    let loanRecord = [];
    let userId;


    onMount(async()=>{
        userId = JSON.parse(localStorage.getItem("userId"));
        books = await fetchBooks();
        loanRecord = await fetchLoanRecord();
    });

    async function fetchLoanRecord(){
        try{
            const token = localStorage.getItem("token");
            console.log(token);
            if(token === "") return; 
            const response = await fetch(
                    loansUrl,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        }
                    }
                );
            if(response.ok){
                const data = await response.json();
                const result = Object.keys(data).map(key => {
                    const entry = data[key];
                    const book = books.find( book => book.book_id == entry.book_id );
                    return {
                        loan_id: entry.id,
                        start_date: entry.date_of_borrow,
                        end_date: entry.date_of_return,
                        deadline: entry.deadline,
                        isReturned: entry.is_book_returned,
                        reader_id: entry.user_id,
                        book_id: entry.book_id,
                        book_info: book? `${book.title}, ${book.author}` : "error"
                    }
                })
                console.log(result);
                return result;
            }else{
                return [];
            }
        }catch(err){
            console.log(err);
        }
    }

    async function fetchBooks(){
        try{
            const token = localStorage.getItem("token");
            if(token === "") return;
            const response = await fetch(
                booksUrl,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                }
                );
            const data = await response.json();
            if(response.ok){
                const result = Object.keys(data).map(key =>{
                    const entry = data[key];
                    return {
                        book_id: entry.id,
                        title: entry.title,
                        author: entry.author,
                        form: entry.is_online,
                        availability: entry.availability,
                        genre: entry.genre
                    }
                })
                return result;
            }
        }catch(err){
            console.log(err);
        }
    }

    async function extendLoan(loan_id){
        if(!userId) return;
        try{
            const queryString = `/${loan_id}?`
            const response = await fetch(extendLoansUrl + queryString, {
                method: 'POST'
            })
            if(response.ok){
                console.log("Przedłużenie przebiegło pomyślnie");
            }else{
                console.log("Nie udalo sie przedłużyć książki");
            }
        }catch(e){
            console.log(e);
        }
    }

    function formatDateString(dateString) {
        const dateObject = new Date(dateString);
        const formattedDate = dateObject.toLocaleDateString();
        return formattedDate;
    }

</script>


<div class=" flex flex-col items-center p-10">
    <table>
        <th>Numer wypożyczenia</th>
        <th>Data wypożyczenia</th>
        <th>Data oddania</th>
        <th>Deadline</th>
        <th>Status</th>
        <th>Książka</th>

        {#each loanRecord as record}
            <tr>

                <td>{record.loan_id}</td>
                <td>{formatDateString(record.start_date)}</td>
                <td>{record.end_date ? record.end_date : ""}</td>
                <td>
                    <div class=" flex flex-row gap-1 justify-center items-center">
                        <h1>{formatDateString(record.deadline)}</h1>
                        {#if !record.isReturned}
                            <button on:click={() => extendLoan(record.loan_id, record.reader_id)}><i class="fa-regular fa-calendar-plus text-lg"></i></button>
                        {/if}
                    </div>
                </td>
                <td>{record.isReturned ? "Zakończone" : "Aktywne"}</td>
                <td>{record.book_info}</td>

            </tr>
        {/each}

    </table>
</div>


<style>

    th, tr, td{
        border: solid 0.5px black;
        padding: 10px;
    }
    
    </style>