<template lang="html">
  <div v-if="editMode" :class="fieldClasses">
    <json-widget v-model="field.wip" :readonly="false" :edit="true" />
    <vk-btn-grp class="btn-ctrls">
      <vk-btn-link class="btn btn-confirm" @click.prevent="commitField">
        <font-awesome-icon icon="check" /> done
        </vk-btn-link>
      <vk-btn-link class="btn btn-cancel" @click.prevent="revertField">
        <font-awesome-icon icon="times" /> cancel
      </vk-btn-link>
    </vk-btn-grp>
  </div>
  <div v-else :class="fieldClasses">
    <json-widget :value="field.value" />
    <a href="#" class="btn-edit" @click.prevent="editField" @focus="editField">
      <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
                         @click="editField" />
    </a>
  </div>
</template>

<script lang="js">
import Vue from 'vue'
import {
  ButtonLink as VkBtnLink,
  ButtonGroup as VkBtnGrp
} from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCheck, faTimes, faEdit, faPlus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ModelFieldMixin } from '@/lib/mixins'
import JsonWidget from '../JsonWidget'

library.add( faCheck, faTimes, faEdit, faPlus );

export default {
  name: 'JsonField',
  mixins: [ ModelFieldMixin ],
  components: {
    VkBtnLink,
    VkBtnGrp,
    JsonWidget,
    FontAwesomeIcon,
  },
  props: {},
  mounted() {
    
  },
  data() {
    return {
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style lang="scss">
.json-field {
  .btn-ctrls {
    display: block;
  }
}
</style>
