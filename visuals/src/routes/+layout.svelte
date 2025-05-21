<script>
    let { children } = $props();
    import "../app.css";
</script>

<div class="px-8 mx-auto sm:max-w-2xl md:max-w-7xl">
    {@render children()}
</div>
