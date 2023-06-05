<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">شارژ موجودی کیف</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> مبلغ (به تومان) <span class="text-red"
                                                            style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.amount"
                     dense/>
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat label="شارژ کیف پول" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>

export default {
  props: ['showDialog', 'form'],

  methods: {
    onSubmit () {
      if (this.form.amount === undefined || this.form.amount === '') {
        this.showNotif('فیلد مبلغ اجباری است')
        return
      }
      if (isNaN(parseInt(this.form.amount))) {
        this.showNotif('لطفا فیلد مبلغ را به صورت عدد صحیح وارد کنید')
        return
      }

      window.location.href = process.env.api + 'payment/panel/wallet/charge/?amount=' + this.form.amount
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-left',
        progress: true
      })
    }
  },

  computed: {
    _dialog: {
      get () {
        return this.showDialog
      },
      set (value) {
        this.$emit('update:showDialog', value)
      }
    }
  }
}
</script>
