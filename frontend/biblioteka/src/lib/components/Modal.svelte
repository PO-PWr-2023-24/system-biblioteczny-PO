<script>
	import { setContext } from "svelte"
	import { isOpen, id } from "../stores/store"
	export let modalId;
	setContext("modalId", modalId)
</script>

<div>
	<slot />
</div>

