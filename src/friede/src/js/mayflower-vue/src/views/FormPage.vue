<template lang="html">
  <section class="form-page">
    <h1>{{ location.title }}</h1>
    <form v-if="model" class="uk-form-stacked">
      <field v-for="field in data.fields" :key="field.meta.name"
             :type="field.meta.type" :name="field.meta.name" :data="field" />
    </form>
  </section>
</template>

<script lang="js">
import Field from '@/components/Field'
import { Model } from '@/lib/objects'
export default  {
  name: 'FormPage',
  components: {
    Field
  },
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
    },
    data() {
      return this.$store.state.modelData || Model( this.model )
    }
  }
}
</script>

<style scoped lang="scss">
  .form-page {

  }
</style>
