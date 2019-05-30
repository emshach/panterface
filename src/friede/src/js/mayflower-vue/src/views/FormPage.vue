<template lang="html">
  <section class="form-page">
    <h1>{{ location.title }}</h1>
    <section v-if="model">
      <h2>Model fields</h2>
      <ul>
        <li v-for="field in model.fields" :key="field.name">
          <b>{{ field.type }}:</b> {{ field.name }}
        </li>
      </ul>
    </section>
  </section>
</template>

<script lang="js">
export default  {
  name: 'form-page',
  props: [],
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
  },
  computed: {
    location() {
      return this.$store.state.location
    },
    model() {
      return this.$store.state.model
    }
  }
}
</script>

<style scoped lang="scss">
  .form-page {

  }
</style>
