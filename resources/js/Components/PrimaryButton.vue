<script setup>
defineProps({
    type: {
        type: String,
        default: 'submit',
    },
});
</script>

<template>
    <button :type="type" class="inline-flex items-center px-4 py-2 bg-green-700 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-green-600 focus:bg-green-700 active:bg-green-900 focus:outline-none focus:ring-2 focus:ring-green-900 focus:ring-offset-2 disabled:opacity-50 transition ease-in-out duration-200">
        <slot />
    </button>
</template>
