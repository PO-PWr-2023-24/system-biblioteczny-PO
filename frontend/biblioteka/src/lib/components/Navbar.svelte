<script>
    import { page } from '$app/stores';  
	import { onMount } from 'svelte';
    let userLogged;

    onMount(()=>{
        userLogged = JSON.parse(localStorage.getItem("userLogged"));
    })

    function logout(){
        userLogged = false;
        localStorage.setItem("userLogged", "false");
    }

</script>
    
    
    <div class=" flex flex-row justify-between items-center p-5 gap-8 bg-slate-300 shadow-md h-24">
        <div class=" flex flex-row gap-2 justify-center items-center">
            <i class="fa-solid fa-book text-4xl"></i>
            <a class=" text-4xl" href="/">Biblioteka</a>
        </div>
        <div class=" flex flex-row justify-center items-center gap-5 p-10">
            {#if userLogged}

                <a 
                    class:border-b-4={$page.url.href?.includes('/books')} 
                    class=" border-white text-4xl hover:text-white" 
                    href="/books"
                >
                    Książki
                </a>
                <a 
                    class:border-b-4={$page.url.href?.includes('/loan-record')} 
                    class=" border-white text-4xl hover:text-white" 
                    href="/loan-record"
                >
                    Wypożyczenia
                </a>
                <button 
                    class=" border-white text-4xl hover:text-white"
                    on:click={logout}
                >
                    Wyloguj
                </button>

            

            {:else}
                <a 
                    class=" border-white text-4xl hover:text-white"
                    href="/login-user"
                >
                    Zaloguj
                </a>
         
            {/if}
            
        </div>
        
        
    </div>