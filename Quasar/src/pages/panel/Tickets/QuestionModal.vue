<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">پرسش جدید برای تیکت &nbsp; '{{ ticket.title }}'</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن سوال <span class="text-red"
                                                     style="font-size: 18px !important;"> * </span></div>
            <q-editor
              height="250px"
              v-model="text"
              :definitions="{
        bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
      }"
            />
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش سوال': 'ثبت سوال'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'ticket', 'question'],

  data () {
    return {
      text: ''
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.text === '<br>' || this.text === '') {
        this.showNotif('لطفا متن سوال را وارد کنید')
        return
      } else {
        this.form.text = this.text
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      if (this.type !== 'create') {
        formData.append('question', this.question.id)
      }

      formData.append('ticket', this.ticket.id)
      formData.append('user', this.$store.state.shop.user.id)

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateQuestion(app, formData)
      } else {
        this.UpdateQuestion(app, formData)
      }
    },

    CreateQuestion (app, formData) {
      this.$axios.post(process.env.api + 'api/panel/tickets/questions/', formData)
        .then(function () {
          app.showNotif('سوال مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateQuestion (app, formData) {
      this.$axios.put(process.env.api + 'api/panel/tickets/questions/' + app.question.id + '/', formData)
        .then(function () {
          app.showNotif('سوال مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        progress: true
      })
    }
  },

  watch: {
    showDialog (value) {
      if (!value) {
        this.text = ''
        this.question = this.question ?? null
      } else {
        if (this.question) {
          this.text = this.question.text
        }
      }
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
