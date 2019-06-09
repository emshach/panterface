<template lang="html">
  <vk-card :class="[ 'form-page', scrolled ]">
    <div slot="header">
      <div class="form-controls uk-align-right uk-text-right">
        <vk-btn type="text" @click.prevent="settings">
          <font-awesome-icon icon="cog" />
        </vk-btn>
        <vk-btn type="text" @click.prevent="discard">
          <font-awesome-icon icon="trash" /> discard
        </vk-btn>
        <vk-btn-grp>
          <vk-btn type="primary" @click.prevent="submit">
            <font-awesome-icon icon="check" /> done
          </vk-btn>
          <vk-btn type="primary" @click.prevent="submitAndRedo">
            <font-awesome-icon icon="plus" /> and another
          </vk-btn>
        </vk-btn-grp>
      </div>
      <vk-card-title class="uk-align-left">{{ location.title }}</vk-card-title>
    </div>
    <vue-perfect-scrollbar class="scroller" slot="body"
                           @ps-scroll-down="scrolled='scrolled'"
                           @ps-y-reach-start="scrolled=''">
      <form v-if="model" class="uk-form-horizontal uk-text-left">
        <field v-for="field in simpleFields" :key="field.meta.name"
               :type="field.meta.type" :name="field.meta.name" :data="field"
               class="uk-margin" />
        <field v-for="field in complexFields" :key="field.meta.name"
               :type="field.meta.type" :name="field.meta.name" :data="field"
               :fieldset="true" />
      </form>
    </vue-perfect-scrollbar>
  </vk-card>
</template>

<script lang="js">
import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { Button as VkBtn, ButtonGroup as VkBtnGrp } from 'vuikit/lib/button'
import { faCheck, faPlus, faTrash, faCog } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Field from '@/components/Field'
import { Model } from '@/lib/objects'

library.add( faCheck, faPlus, faTrash, faCog )

export default  {
  name: 'FormPage',
  components: {
    VuePerfectScrollbar,
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
      data: null,
      scrolled: ''
    }
  },
  methods: {
    settings() {
    },
    submit() {
    },
    submitAndRedo() {
    },
    discard() {
    }
  },
  computed: {
    model() {
      return this.$store.state.model;
    },
    modelData() {
      if ( this.data )
        return this.data;
      if ( this.$store.state.modelData )
        this.data = this.$store.state.modelData;
      else if ( this.model )
        this.data = Model( this.model );
      return this.data || { fields: [] };
    },
    location() {
      return this.$store.state.location
    },
    simpleFields() {
      return this.modelData.fields.filter(
        x => !x.meta.related || !x.meta.type.match( /Multiple|Choices/ ));
    },
    complexFields() {
      return this.modelData.fields.filter(
        x => x.meta.related && x.meta.type.match( /Multiple|Choices/ ));
    }
  }
}
</script>

<style lang="scss">
.form-page {
  border-radius: 2px;
  height: 100%;
  > .uk-card-header {
    padding: 0;
    border-bottom: none;
    .uk-card-title{
      margin: 6px 14px;
    }
    .form-controls{
      margin-bottom: 0;
    }
    .uk-button {
      font-size: 0.95rem;
      line-height: 34px;
      padding: 0 12px;
    }
    .uk-button-group {
      .uk-button:first-child {
        /* border-top-left-radius: 2px; */
        border-bottom-left-radius: 2px;
      }
      .uk-button:last-child {
        border-top-right-radius: 2px;
        /* border-bottom-right-radius: 2px; */
      }
    }
  }
  .uk-input, .uk-select, .uk-textarea {
    border: 1px solid #e5e5e5;
  }
  .uk-card-body {
    height: calc( 100% - 45px );
    box-sizing: border-box;
    padding: 6px 0px 1px 24px;
    > .scroller {
      height: 100%;
      padding-right: 16px;
    }
  }
  &.scrolled .uk-card-body {
    box-shadow: inset 0 12px 11px -11px rgba(0, 0, 0, 0.1);
  }
  .no-data {
    color: rgba(0,0,0,0.35);
  }
  .btn-confirm {
    color: limegreen;
    &:hover {
      color: forestgreen;
    }
  }
  .btn-cancel {
    color: red;
    &:hover {
      color: darkred;
    }
  }
}
</style>
