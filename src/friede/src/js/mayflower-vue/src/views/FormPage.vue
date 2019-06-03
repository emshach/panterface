<template lang="html">
  <vk-card class="form-page">
    <vk-card-title slot="header">{{ location.title }}</vk-card-title>
    <form slot="body" v-if="model" class="uk-form-horizontal uk-text-left">
      <field v-for="field in data.fields" :key="field.meta.name"
             :type="field.meta.type" :name="field.meta.name" :data="field"
             class="uk-margin" />
    </form>
    <div class="form-controls uk-text-right">
      <vk-btn type="text" class="uk-margin-right" @click.stop="cancel">cancel</vk-btn>
      <vk-btn-grp>
        <vk-btn type="primary" @click.stop="submit">Save</vk-btn>
        <vk-btn @click.stop="submitAndRedo">Add another</vk-btn>
      </vk-btn-grp>
    </div>
  </vk-card>
</template>

<script lang="js">
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { Button as VkBtn, ButtonGroup as VkBtnGrp } from 'vuikit/lib/button'
import Field from '@/components/Field'
import { Model } from '@/lib/objects'
export default  {
  name: 'FormPage',
  components: {
    VkCard,
    VkCardTitle,
    VkBtn,
    VkBtnGrp,
    Field
  },
  mounted() {
  },
  data() {
    return {
    }
  },
  methods: {
    submit() {
    },
    submitAndRedo() {
    },
    cancel() {
    }
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

<style lang="scss">
.form-page {
  margin: 40px 20px;
  border-radius: 2px;
  .uk-input, .uk-select, .uk-textarea {
    border: 1px solid #e5e5e5;
  }
  .no-data {
    color: rgba(0,0,0,0.35);
  }
}
.uk-button-group .uk-button:first-child {
  border-top-left-radius: 2px;
  border-bottom-left-radius: 2px;
}
.uk-button-group .uk-button:last-child {
  border-top-right-radius: 2px;
  border-bottom-right-radius: 2px;
}
</style>
