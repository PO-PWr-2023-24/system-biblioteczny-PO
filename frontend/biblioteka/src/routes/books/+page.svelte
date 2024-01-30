<script >
	import { onMount } from "svelte";
    import Modal from "../../lib/components/Modal.svelte"
	import Trigger from "../../lib/components/Trigger.svelte"
	import Content from "../../lib/components/Content.svelte"

    const booksUrl = "http://127.0.0.1:8000/api/books";
    const borrowUrl = "http://127.0.0.1:8000/borrow/1/new";
    const reserveBookUrl = "http://127.0.0.1:8000/api/reservation" 
    let books = [];
    let message = "";

    let userId;

    onMount(async ()=>{
        books = await fetchBooks();
        userId = JSON.parse(localStorage.getItem("userId")); 
    });

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

    async function rentOnline(book_id){
        try{
            const token = localStorage.getItem("token");
            if(token === "") return;
            const currentDate = new Date();
            const deadlineDate = new Date(currentDate);
            deadlineDate.setDate(currentDate.getDate() + 14);
            let formattedStartDate = getFormattedDate(currentDate);
            let formattedDeadline = getFormattedDate(deadlineDate)
            const response = await fetch(borrowUrl, {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                body:JSON.stringify({
                    book_id: book_id,
                    date_of_borrow: formattedStartDate,
                    deadline: formattedDeadline
                })
            })
            if(response.ok){
                console.log("Rezerwacja przebiegła pomyślnie");
            }else{
                console.log("Nie udalo sie zarezerwowac");
            }
            const book = books.find( book => book.book_id == book_id );
            console.log(book);
            if(book !== -1) message = "Pomyślnie wypożyczono książkę " + book.title;
            books = await fetchBooks();
        }catch(e){
            console.log(e);
        }
    }

    async function makeReservation(book_id){
        try{
            const token = localStorage.getItem("token");
            if(token === "") return;
            const response = await fetch(reserveBookUrl + `/${book_id}/`, {
                method: 'POST',
                headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
            })
            if(response.ok){
                console.log("Rezerwacja przebiegła pomyślnie");
            }else{
                console.log("Nie udalo sie zarezerwowac");
            }
            const book = books.find( book => book.book_id == book_id );
            console.log(book);
            if(book !== -1) message = "Pomyślnie zarezerwowano książkę " + book.title;
            books = await fetchBooks();
        }catch(e){
            console.log(e);
        }
    }  
    function getFormattedDate(currentDate) {
       
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0');
        const day = String(currentDate.getDate()).padStart(2, '0');
        const hours = String(currentDate.getHours()).padStart(2, '0');
        const minutes = String(currentDate.getMinutes()).padStart(2, '0');
        const seconds = String(currentDate.getSeconds()).padStart(2, '0');
        const milliseconds = String(currentDate.getMilliseconds()).padStart(3, '0');

        const timezoneOffset = -currentDate.getTimezoneOffset();
        const timezoneOffsetHours = Math.floor(Math.abs(timezoneOffset) / 60).toString().padStart(2, '0');
        const timezoneOffsetMinutes = (Math.abs(timezoneOffset) % 60).toString().padStart(2, '0');
        const timezone = timezoneOffset >= 0 ? `+${timezoneOffsetHours}:${timezoneOffsetMinutes}` : `-${timezoneOffsetHours}:${timezoneOffsetMinutes}`;

        const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}${timezone}`;

        return formattedDate;
    }

</script>


<div class=" items-center flex flex-col p-10">

    <table class=" border-[0.5px] border-black">

        <th>Tytuł</th>
        <th>Autor</th>
        <th>Gatunek</th>
        <th>Forma</th>
        <th>Dostępność</th>

        {#each books as book}
            <tr>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.genre}</td>
                <td>{book.form ? "Elektroniczna" : "Papierowa"}</td>
                <td>{book.availability ? "Dostępna" : "Niedostępna"}</td>
                <td>
                    <div>
                        {#if book.form && book.availability}
                            <Modal modalId={`book:${book.id}form:${book.form}`}>
                                <Content>
                                    <div class=" flex flex-col gap-2 justify-center items-center">
                                        <h1 class=" bg-slate-300 p-2">
                                            Informacja
                                        </h1>
                                        <p>
                                            {`Zamierzasz wypożyczyć ${book.title} autora ${book.author}. Materiały online dostępne są w zakładce Moje Konto.`}
                                        </p>
                                        <button class=" border-green-500 border-2 p-2 rounded-md" on:click={() => rentOnline(book.book_id)}>
                                            Potwierdź
                                        </button>
                                    </div>
                                </Content>
                                <Trigger>
                                    <button class=" bg-slate-300 p-1 rounded-md">
                                        Wypożycz Online
                                    </button>
                                </Trigger>
                            </Modal>
                        {:else if !book.form && book.availability}
                            <Modal modalId={book.book_id}>
                                <Content>
                                    <div class=" flex flex-col gap-2 justify-center items-center">
                                        <h1 class=" bg-slate-300 p-2">
                                            Informacja
                                        </h1>
                                        <p>
                                            {`Zamierzasz zarezerwować ${book.title} autora ${book.author}. Jesteś pewien?`}
                                        </p>
                                        <button class=" border-green-500 border-2 p-2 rounded-md" on:click={() => makeReservation(book.book_id)}>
                                            Potwierdź
                                        </button>
                                    </div>
                                </Content>
                                <Trigger>
                                    <button class=" bg-slate-300 p-1 rounded-md">
                                        Rezerwuj
                                    </button>
                                </Trigger>
                            </Modal>
                        {/if}
                    </div>
                </td>
            </tr>
        {/each}

    </table>
    {#if message.length !== 0}
        <h1 class=" text-green-400">{message}</h1>
    {/if}

</div>


<style>

th, tr, td{
    border: solid 0.5px black;
    padding: 10px;
}

</style>