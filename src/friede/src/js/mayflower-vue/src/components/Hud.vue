<template>
<div :id="'hud-' + getHudId()" class="hud">
  <mouse-overlay></mouse-overlay>
  <guage v-for="( guage, index ) in guages" :key=index :options=guage></guage>
  <hud-action v-for"( action, name ) in actions" :key=name :options=action></hud-action>
</div>
</template>

<script>
export default {
  data() {
    return {
      guages: [],
      actions: {}
    };
  }
};
</script>

<style scoped>

</style>
