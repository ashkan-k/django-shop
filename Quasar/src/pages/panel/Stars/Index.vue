<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="stars_list" icon="mdi-format-list-text" label="امتیازات شما"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="stars_list">
            <q-input style="max-width: 300px !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pa-md">
              <q-table
                :data="data"
                :columns="columns"
                :loading="loading"
                row-key="id"
                :rows-per-page-options="[10]"
                binary-state-sort
                flat
                separator="horizontal"
                color="brand"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="id">{{ props.rowIndex + 1 }}</q-td>
                    <q-td key="score">
                      <q-input type="number" v-if="is_edit_mode && current_row_number === props.rowIndex" rounded
                               outlined
                               style="width: 250px !important; height: 30px !important;" v-model="new_score"/>
                      <p v-else>{{ props.row.score }}</p>
                    </q-td>
                    <q-td key="product">{{ props.row.product.title }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.product.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="setting">
                      <div v-if="is_edit_mode && current_row_number === props.rowIndex">
                        <q-btn @click="EditStar(props.row.id)" style="color: green" rounded
                               icon="mdi-shield-check-outline" label="ذخیره" size="md" flat
                               dense>
                          <q-tooltip>ذخیره</q-tooltip>
                        </q-btn>
                        |
                        <q-btn @click="ShowEditBox(props.row.score , null)" style="color: red" rounded
                               icon="mdi-close-outline" label="لغو" size="md" flat
                               dense>
                          <q-tooltip>لغو</q-tooltip>
                        </q-btn>
                      </div>
                      <div v-else>
                        <q-btn @click="ShowEditBox(props.row.score , props.rowIndex)" style="color: #4facfe" rounded
                               icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                               dense>
                          <q-tooltip>ویرایش</q-tooltip>
                        </q-btn>
                        |
                        <q-btn
                          @click="DeleteStar(props.row.product.title , props.row.id)"
                          style="color: red" rounded
                          icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                          <q-tooltip>حذف</q-tooltip>
                        </q-btn>
                      </div>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>

              <div class="row justify-center q-mt-md" style="direction: ltr">
                <q-pagination v-model="paginationPage" color="teal" :max="lastPage" :max-pages="6"
                              :boundary-numbers="true" size="sm"/>
              </div>

            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  data () {
    return {
      search: '',

      data: [],

      new_score: 0,
      is_edit_mode: false,
      current_row_number: null,

      paginationPage: 1,
      lastPage: 0,

      loading: false,
      columns: [
        {
          name: 'id',
          required: true,
          label: 'ردیف',
          align: 'left',
          field: row => row.name,
          sortable: true
        },
        {
          name: 'score',
          align: 'left',
          label: 'امتیاز',
          field: 'score',
          sortable: true
        },
        {
          name: 'product',
          align: 'left',
          label: 'محصول',
          field: 'product',
          sortable: true
        },
        {
          name: 'original_image',
          align: 'left',
          label: 'عکس محصول',
          field: 'original_image',
          sortable: true
        },
        {
          name: 'setting',
          align: 'left',
          label: 'عملیات',
          field: 'setting',
          sortable: true
        }
      ],

      tab: 'stars_list',
      splitterModel: 20,
      showDialog: false
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  methods: {
    ShowImage (url) {
      return url.replace('http://localhost:8000/', process.env.api)
    },

    showNotif (message, icon = 'error', color = 'red', time = 3000) {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        timeout: time,
        progress: true
      })
    },

    DeleteStar (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید امتیاز شما به محصول ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
        ok: {
          push: true,
          label: 'تایید'
        },
        cancel: {
          push: true,
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        app.$axios.delete(process.env.api + 'api/panel/stars/' + id)
          .then(function () {
            app.showNotif('امتیاز مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllStars()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    ShowEditBox (score = 0, rowIndex) {
      this.new_score = score
      this.current_row_number = rowIndex
      this.is_edit_mode = rowIndex !== null
    },

    EditStar (id) {
      const app = this

      if (this.new_score <= 0) {
        app.showNotif('امتیاز شما نمیتواند کمتر از 0 باشد')
        return
      }

      if (this.new_score > 5) {
        app.showNotif('امتیاز شما نمیتواند بیشتر از 5 باشد')
        return
      }

      const formData = new FormData()
      formData.append('score', this.new_score)

      this.$q.loading.show()
      this.$axios.put(process.env.api + 'api/panel/stars/' + id + '/', formData)
        .then(function () {
          app.showNotif('امتیاز مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline', 'green')
          app.is_edit_mode = !app.is_edit_mode
          app.rowIndex = 0
          app.GetAllStars()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    },

    GetAllStars () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/stars/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    }
  },

  watch: {
    search () {
      this.GetAllStars()
    },
    paginationPage () {
      this.GetAllStars()
    }
  },

  mounted () {
    this.GetAllStars()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
