<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="comments" icon="mdi-format-list-text"
                 label="نظرات شما"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="comments">
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
                    <q-td key="title">{{ props.row.title }}</q-td>
                    <q-td key="text">{{ props.row.text.slice(0, 20) + '...' }}</q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="ShowText(props.row.text)"
                        rounded
                        icon="mdi-comment-eye" label="نمایش متن" size="md" flat
                        dense>
                        <q-tooltip>نمایش متن</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="EditComment(props.row.id , props.row.user , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteComment(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
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

        <Modal :showDialog.sync="showDialog" :form="form"></Modal>
        <CommentDetail :show-comment-detail.sync="showCommentDetail" :body="text"></CommentDetail>

      </q-card>
    </div>
  </div>
</template>

<script>
import Modal from './Modal'
import CommentDetail from './CommentDetail'
import moment from 'moment'

export default {
  components: {
    Modal: Modal,
    CommentDetail: CommentDetail
  },

  data () {
    return {
      form: {},
      text: '',

      search: '',

      data: [],

      paginationPage: 1,
      lastPage: 0,
      pages_count: 0,

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
          name: 'title',
          align: 'left',
          label: 'عنوان',
          field: 'title',
          sortable: true
        },
        {
          name: 'text',
          align: 'left',
          label: 'متن',
          field: 'text',
          sortable: true
        },
        {
          name: 'status',
          align: 'left',
          label: 'وضعیت',
          field: 'status',
          sortable: true
        },
        {
          name: 'created_at',
          align: 'left',
          label: 'تاریخ ثبت',
          field: 'created_at',
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

      tab: 'comments',
      splitterModel: 20,
      showDialog: false,
      showCommentDetail: false
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  methods: {
    ShowStatus (status) {
      if (status) {
        return 'تایید شده'
      }
      return 'تایید نشده'
    },

    ShowStatusColor (status) {
      if (status) {
        return 'secondary'
      }
      return 'red'
    },

    ShowText (text) {
      this.text = text
      this.showCommentDetail = true
    },

    setDialog () {
      this.showDialog = true
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

    DeleteComment (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید نظر' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/panel/comments/' + id)
          .then(function () {
            app.showNotif('نظر انتخابی شما با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllComments()
            }
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditComment (id) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/panel/comments/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.setDialog()

          app.$q.loading.hide()
        })
    },

    GetAllComments () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/comments/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    }
  },

  watch: {
    search () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllComments()
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllComments()
    }
  },
  mounted () {
    this.GetAllComments()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
