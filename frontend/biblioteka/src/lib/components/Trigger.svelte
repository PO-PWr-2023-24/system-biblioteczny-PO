<script>
	import { isOpen, id } from "../stores/store"
	import { getContext } from "svelte"
	const modalId = getContext("modalId")
</script>
<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<span on:click={() => $id = modalId}>
	<slot />
</span>

<style>
	span:hover	 {
		cursor: pointer;
	}
</style>