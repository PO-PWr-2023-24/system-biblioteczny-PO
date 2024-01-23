<script >
	import { onMount } from "svelte";

    let booksUrl = "";
    let editBooksUrl = "";
    let loanRecordUrl = "";
    let books = [];

    let userId;

    onMount(async ()=>{
        books = await fetchBooks();
        userId = JSON.parse(localStorage.getItem("userId")); 
    });

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
        return [{book_id: 1, title: "Unbearable lightness of Being", author: "Kundera Milan", form: "digital", availability: "available"}, {book_id: 1, title: "Fairy Tale", author: "Stephen King", form: "paper", availability: "available"}];
    }

    async function rentOnline(book_id){
        try{
            const queryString = `/${book_id}?`
            const response = await fetch(editBooksUrl + queryString, {
                method: 'POST'
            })
            if(response.ok){
                console.log("Rezerwacja przebiegła pomyślnie");
            }else{
                console.log("Nie udalo sie zarezerwowac");
            }
        }catch(e){
            console.log(e);
        }
    }

    async function makeReservation(book_id){
        try{
            const queryString = `/${book_id}?`
            const response = await fetch(editBooksUrl + queryString, {
                method: 'POST'
            })
            if(response.ok){
                console.log("Rezerwacja przebiegła pomyślnie");
            }else{
                console.log("Nie udalo sie zarezerwowac");
            }
        }catch(e){
            console.log(e);
        }
    }

</script>


<div class=" items-center flex flex-col p-10">

    <table class=" border-[0.5px] border-black">

        <th>Tytuł</th>
        <th>Autor</th>
        <th>Forma</th>
        <th>Dostępność</th>
        <th></th>


        {#each books as book}
            <tr>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.form}</td>
                <td>{book.availability}</td>
                <td>
                    <div>
                        {#if book.form === "digital" && book.availability === "available"}
                            <button 
                                class=" bg-slate-300 p-1 rounded-md"
                                on:click={() => rentOnline(book.book_id)}    
                            >
                                Wypożycz Online
                            </button>
                        {:else if book.form === "paper" && book.availability == "available"}
                            <button 
                                class=" bg-slate-300 p-1 rounded-md"
                                on:click={() => makeReservation(book.book_id)}
                            >
                                Rezerwuj
                            </button>
                        {/if}
                    </div>
                </td>
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