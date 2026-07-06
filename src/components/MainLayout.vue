<template>
  <main class="main">
    <router-view v-slot="{ Component }">
      <transition name="page" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
</template>

<style scoped>
.main {
  margin-left: var(--sidenav-w);
  margin-top: var(--topnav-h);
  min-height: calc(100vh - var(--topnav-h));
  padding: var(--space-8);
  overflow-y: auto;
  height: calc(100vh - var(--topnav-h));
}
</style>
