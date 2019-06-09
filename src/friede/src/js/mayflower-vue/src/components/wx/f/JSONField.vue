<template lang="html">
  <div v-if="editMode" :class="fieldClasses">
    <json-widget v-model="field.wip" :readonly="false"
                 :edit="true" />
    <vk-btn-grp>
      <vk-btn-link class="btn btn-confirm" @click.prevent="commitField">
        <font-awesome-icon icon="check" /> done
      </vk-btn-link>
      <vk-btn-link class="btn btn-cancel" @click.prevent="revertField">
        <font-awesome-icon icon="times" /> cancel
      </vk-btn-link>
    </vk-btn-grp>
  </div>
  <a v-else :class="fieldClasses" @click.prevent="editField" @focus="editField">
    <json-widget :value="field.value" />
    <font-awesome-icon v-if="!readonly" :icon="isset ? 'edit': 'plus'"
                       @click="editField" />
  </a>
</template>

<script lang="js">
import Vue from 'vue'
import {
  ButtonLink as VkBtnLink,
  ButtonGroup as VkBtnGrp
} from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCheck, faTimes} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ModelFieldMixin } from '@/lib/mixins'
import JsonWidget from '../JsonWidget'

library.add( faCheck, faTimes );

export default {
  name: 'JsonField',
  mixins: [ ModelFieldMixin ],
  components: {
    JsonWidget,
    FontAwesomeIcon,
  },
  props: {},
  mounted() {
    
  },
  data() {
    return {
      options: {
        confirmText: 'confirm',
        cancelText: 'cancel'
      }
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
  .json-field {

  }
</style>
