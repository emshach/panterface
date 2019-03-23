<template lang="html">
<form id="prompt" @submit.prevent="submit" class="uk-flex uk-wrap-around">
  <Breadcrumb/>
  <input id="cli" name="cli" class="uk-input uk-flex-1" v-model="cli" @input="input" />
</form>
</template>

<script lang="js">
export default  {
  name: 'prompt',
  props: [],
  mounted() {

  },
  data() {
    return {
      cli: ''
    }
  },
  methods: {
    submit() {
    },
    input() {
    }
  },
  computed: {

  },
}
</script>

<style scoped lang="scss">
  .prompt {

  }
</style>
