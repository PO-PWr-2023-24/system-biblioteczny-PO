<script >
	import { onMount } from "svelte";

    let loansUrl = "";
    let bookUrl = "";
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
        // try{
        //     const response = await fetch(loansUrl);
        //     const data = await response.json();
        //     const result = Object.keys(data).map(key => {
        //         const entry = data[key];
        //         const book = books.find( book => book.book_id == entry.book_id );
        //         return {
        //             loan_id: key,
        //             start_date: entry.start_date,
        //             end_date: entry.end_date,
        //             deadline: entry.deadline,
        //             status: entry.status,
        //             reader_id: entry.user_id,
        //             book_id: entry.book_id,
        //             book_info: book? `${book.title}, ${book.author}` : "error"
        //         }
        //     })
        //     return result;
        // }catch(err){
        //     console.log(err);
        // }
        return [{loan_id: 1, start_date: "23.01.2024", end_date: "", deadline: "06.02.2024", status: "active", reader_id: 1, book_id: 1, book_info: "Fairy Tale, Stephen King"}];
    }

    async function fetchBooks(){
            // try{
        //     const response = await fetch(booksUrl);
        //     const data = await response.json();
        //     const result = Object.keys(data).map(key => {
        //         const entry = data[key];
        //         return {
        //             book_id: key,
        //             title: entry.title,
        //             author: entry.author,
        //             form: entry.form,
        //             availability: entry.availability
        //         }
        //     })
        //     return result;
        // }catch(err){
        //     console.log(err);
        // }
        return [{book_id: 1, title: "Unbearable lightness of Being", author: "Kundera Milan", form: "digital", availability: "available"}, {book_id: 1, title: "Fairy Tale", author: "Stephen King", form: "paper", availability: "unavailable"}];
   
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
                <td>{record.start_date}</td>
                <td>{record.end_date}</td>
                <td>
                    <div class=" flex flex-row gap-1 justify-center items-center">
                        <h1>{record.deadline}</h1>
                        {#if record.status === "active"}
                            <button on:click={() => extendLoan(record.loan_id, record.reader_id)}><i class="fa-regular fa-calendar-plus text-lg"></i></button>
                        {/if}
                    </div>
                </td>
                <td>{record.status}</td>
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