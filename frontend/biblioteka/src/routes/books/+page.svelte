<script>
	import { onMount } from "svelte";

    let booksUrl = ""
    let books = [];

    onMount(()=>{
        books = fetchBooks();
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
            
        return [{book_id: 1, title: "Unbearable lightness of Being", author: "Kundera Milan", form: "digital", availability: "available"}];

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
                        {#if book.form === "digital"}
                            <button>
                                Wypożycz Online
                            </button>
                        {:else}
                            <button>
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

th{
    border: solid 0.5px black;
    padding: 10px;
}

</style>