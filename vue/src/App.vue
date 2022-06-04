<script>
export default {
  computed: {
    isHome(){
      return this.$route.name == 'home';
    }
  }
}
</script>
<template>
  <div id="nav">
    <router-link v-if="!isHome" to="/">Home</router-link>
  </div>
  <router-view/>
</template>