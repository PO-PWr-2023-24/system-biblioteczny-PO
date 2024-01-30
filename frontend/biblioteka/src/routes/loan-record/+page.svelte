<script >
	import { onMount } from "svelte";

    const loansUrl = "http://127.0.0.1:8000/borrow/1";
    const booksUrl = "http://127.0.0.1:8000/api/books";
    const extendLoansUrl = "http://127.0.0.1:8000/borrow";
    const reservationsUrl = "http://127.0.0.1:8000/api/reservations"
    let books = [];
    let loanRecord = [];
    let reservations = [];
    let userId;
    let extendMessage = "";
    let extendError = "";


    onMount(async()=>{
        userId = JSON.parse(localStorage.getItem("userId"));
        books = await fetchBooks();
        loanRecord = await fetchLoanRecord();
        reservations = await fetchReservations();
    });

    async function fetchLoanRecord(){
        try{
            const token = localStorage.getItem("token");
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

    async function fetchReservations(){
        try{
            const token = localStorage.getItem("token");
            if(token === "") return;
            const response = await fetch(
                reservationsUrl + "/",
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    mode: 'cors'
                }
                );
            const data = await response.json();
            if(response.ok){
                const result = Object.keys(data).map(key =>{
                    const entry = data[key];
                    return {
                        reservationDate: entry.reservationDate,
                        bookId: entry.bookId,
                        bookTitle: entry.bookTitle,
                    }
                })
                return result;
            }else{
                return [];
            }
        }catch(err){
            console.log(err);
            return [];
        }
    }

    async function extendLoan(loan_id){
        try{
            const token = localStorage.getItem("token");
            if(token === "") return;
            const borrow = loanRecord.find(loan => loan.loan_id == loan_id);
            const currentDate = new Date(borrow.deadline);
            const newDeadlineDate = new Date(currentDate);
            newDeadlineDate.setDate(currentDate.getDate() + 7);
            let formattedDeadline = newDeadlineDate.toISOString();
            console.log(formattedDeadline);
            const response = await fetch(
                extendLoansUrl + `/${loan_id}/extend`,
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body:JSON.stringify({
                        deadline: formattedDeadline
                    })
                }
                );
            if(response.ok){
                console.log("OK")
                extendMessage = "Pomyślnie przedłużono do dnia " + formatDateString(formattedDeadline);
                extendError = "";
            }else{
                console.log("NIEOK")
                extendError = "Nie można przedłużyć tego wypożyczenia.";
                extendMessage = "";
            }
        }catch(err){
            console.log(err);
        }
    }

    function formatDateString(dateString) {
        const dateObject = new Date(dateString);
        const formattedDate = dateObject.toLocaleDateString();
        return formattedDate;
    }
    
</script>

<div class=" flex flex-col gap-2 p-10 justify-center">
    <h1 class=" text-2xl"><strong>Wypożyczenia</strong></h1>
    <div class=" flex flex-col items-center">
    
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
        {#if extendMessage.length !== 0}
        <h1 class=" text-green-500">{extendMessage}</h1>
        {/if}

        {#if extendError.length !== 0}
            <h1 class=" text-red-600">{extendError}</h1>
        {/if}
        
    </div>
    <h1 class=" text-2xl pt-10"><strong>Rezerwacje</strong></h1>
    <div class=" flex flex-col items-center">
    
        <table>
            <th>Numer rezerwacji</th>
            <th>Data rezerwacji</th>
            <th>Książka</th>
    
            {#each reservations as reservation, i}
                <tr>
                    <td>{i}</td>
                    <td>{formatDateString(reservation.reservationDate)}</td>
                    <td>{reservation.bookTitle}</td>
                </tr>
            {/each}
    
        </table>
    </div>
</div>



<style>

    th, tr, td{
        border: solid 0.5px black;
        padding: 10px;
    }
    
    </style>