<script>
	import { onMount } from "svelte";
    import { page } from '$app/stores';  
    import "../app.css";
    import Navbar from "../lib/components/Navbar.svelte";

    let userLogged;

    onMount(()=>{
        userLogged = JSON.parse(localStorage.getItem("userLogged"));

        if(!userLogged && ($page.url.href?.includes('/books') || $page.url.href?.includes('/loan-record'))){
            window.location.href = "/";
        }
    })

</script>

<Navbar></Navbar>
<slot/>