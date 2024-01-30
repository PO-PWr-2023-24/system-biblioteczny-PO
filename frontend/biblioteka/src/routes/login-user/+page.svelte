<script>
let email = '';
let password = '';
let error = '';

let loginUrl = "http://127.0.0.1:8000/api/login";

async function login(){
    try{
        const response = await fetch(loginUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: email,
                password: password
            })
        })
        if(response.ok){
            localStorage.setItem("userLogged", "true");
            const responseData = await response.json();
            localStorage.setItem("token", responseData.token);
            window.location.href = "/";
        }else{
            error = "Niepoprawny email lub hasło."
        }
    }catch(e){
        error = "Błąd logowania";
        console.log(e);
    }    
}

</script>


<div class="  fixed flex flex-col justify-center items-center top-0 left-0 h-full w-full z-[99] bg-white">
    <form on:submit|preventDefault={login} class=" bg-slate-300 bg-opacity-75 w-[500px] h-[700px] shadow-xl rounded-md flex flex-col justify-center items-center p-4 gap-5">
        
        <div class=" flex flex-row justify-center items-center">
            <i class="fa-solid fa-book text-4xl"></i>
            <a href="/"><h1 class=" text-4xl">Biblioteka</h1></a>
        </div>
        <div class=" flex flex-col gap-2">
            <label for="email" class=" text-3xl">E-mail</label>
            <input 
                type="email" 
                bind:value={email} 
                placeholder="example@gmail.com" 
                id="email" 
                name="email"
                class=" text-4xl rounded-lg p-4"
            >
        </div>
        <div class=" flex flex-col gap-2">
            <label for="password" class=" text-3xl">Password</label>
            <input 
                type="password" 
                bind:value={password} 
                placeholder="Password"
                id="password" 
                name="password"
                class=" text-4xl rounded-lg p-4"
            >
        </div>
        {#if error !== ''}
            <h2 class=" text-red-600"> {error}</h2>
        {/if}
        <button type="submit" class=" text-4xl hover:text-white">
            Zaloguj
        </button>
        
    </form>
</div>