<template>
    <Navbar :links="navLinks" />
    <main style="padding-top: 60px">
        <router-view />
    </main>
</template>

<script setup>
import Navbar from "./components/Navbar.vue";

const navLinks = [
    { text: "Home", href: "/" },
    { text: "About", href: "/about" },
    { text: "Contact", href: "/contact" },
];
</script>
