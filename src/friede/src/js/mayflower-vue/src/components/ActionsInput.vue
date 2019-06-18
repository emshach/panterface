<template lang="html">
  <div class="actions-input">
    <select @select.native=input v-model=action >
      <option value="">do something</option>
      <option v-for="a in actions" :key=a :value=a >{{a}}</option>
    </select>
  </div>
</template>

<script lang="js">
  export default {
    name: 'actions-input',
    props: {
      actions: {
        type: Array,
        default: () => []
      }
    },
    mounted() {
    },
    data() {
      return {
        action: ''
      }
    },
    methods: {
      input(e) {
        this.$emit( this.action );
      }
    },
    computed: {}
}
</script>

<style scoped lang="scss">
  .actions-input {

  }
</style>
