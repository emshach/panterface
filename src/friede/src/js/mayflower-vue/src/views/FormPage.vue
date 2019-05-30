<template lang="html">
  <vk-card class="form-page">
    <vk-card-title slot="header">{{ location.title }}</vk-card-title>
    <form v-if="model" class="uk-form-stacked">
      <field v-for="field in data.fields" :key="field.meta.name"
             :type="field.meta.type" :name="field.meta.name" :data="field" />
    </form>
  </vk-card>
</template>

<script lang="js">
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import Field from '@/components/Field'
import { Model } from '@/lib/objects'
export default  {
  name: 'FormPage',
  components: {
    VkCard,
    VkCardTitle,
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
