<template>
  <div class="q-pa-md">
    <q-dialog v-model="_dialog">
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pa-sm q-mb-sm">
          <div class="q-ml-sm-sm">جزییات متن</div>
          <q-space/>
          <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
                 v-close-popup/>
        </q-card-section>

        <q-card-section class="items-center">
          <q-separator></q-separator>
              <p style="margin: 0 auto ; padding-top: 20px !important; padding-bottom: 20px !important;"> {{ body }} </p>
          <q-separator></q-separator>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>
<script>
export default {
  props: ['showCommentDetail', 'body'],

  computed: {
    _dialog: {
      get () {
        return this.showCommentDetail
      },
      set (value) {
        this.$emit('update:showCommentDetail', value)
      }
    }
  }
}
</script>
