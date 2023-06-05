a
<template>
  <q-page class="q-pa-sm">
    <div class="row q-col-gutter-sm" style="margin: 10px 12px !important;">
      <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12">
        <q-card class="bg-white text-black ">
          <br>
          <h5 align="center"> تیکت &nbsp; '{{ ticket.title }}' </h5>
          <q-separator class="bg-info" style="margin: 20px auto; width: 50% !important;"></q-separator>
          <div class="faqs-inner">
            <q-banner v-if="!ticket.status" rounded style="margin: 50px auto !important;"
                      class="col-md-11 col-sm-11 col-xs-11 bg-warning shadow-3">
              <template v-slot:avatar>
                <q-icon name="mdi-alert-box" color="red"/>
              </template>
              <p style="text-align: center">این تیکت قبلا توسط کاربر {{ ticket.user ? ticket.user.username : '' }} بسته شده است</p>
            </q-banner>
            <div v-for="(question, index) in ticket.questions" :key="index" class="faq-item" style="margin: 20px 20px;">
              <div>
                <div class="faq-item-inner">
                  <div class="user-image">
                    <img :src="ShowImage(ticket.user.image)" alt="user-name"/>
                  </div>
                  <div class="user-text">
                    <h6 style="margin: 11px 0 23px;">{{ ticket.user.username }}
                      ({{ CheckIsSupporterOrSuperUser() ? 'کاربر' : 'شما' }})</h6>
                    <q-btn v-if="CheckIsSupporterOrSuperUser() && ticket.status" style="float: left !important;"
                           @click="setAnswerDialog('create' , question)" rounded color="secondary" label="پاسخ"/>
                    <div class="text" v-html="question.text"></div>
                    <div class="user-footer">
                      <div class="date-content">
                        <div class="date">{{ question.created_at | FormatDate }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <div v-for="(answer, index2) in ShowCurrentAnswer(question)" :key="index2"
                     class="faq-answers  shadow-3">
                  <div class="faq-answers-inner">
                    <div class="user-image">
                      <img src="http://getdrawings.com/free-icon-bw/support-icons-8.png" alt="user-name"/>
                    </div>
                    <div class="user-text">
                      <h6 style="margin: 8px 0 23px;">
                        مسئول پاسخ ({{ CheckIsSupporterOrSuperUser() ? 'شما' : 'پشتیبانی سایت' }})</h6>

                      <div v-if="ticket.status">
                        <q-btn v-if="CheckIsSupporterOrSuperUser()" style="float: left !important;"
                               @click="EditAnswers(answer.id , question)" rounded color="green" label="ویرایش"/>
                        <q-btn v-if="CheckIsSupporterOrSuperUser()" style="float: left !important;"
                               @click="DeleteAnswer(answer.id)" rounded color="red" label="حذف"/>
                      </div>

                      <div class="text" v-html="answer.text"></div>
                      <div class="user-footer">
                        <div class="date-content">
                          <div class="date">{{ answer.created_at | FormatDate }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <q-separator class="bg-grey" style="margin: 50px auto; width: 80% !important;"></q-separator>
            </div>
            <br>
          </div>

          <div class="q-pa-md q-mt-lg q-gutter-sm">
            <q-btn rounded color="red" @click="$router.back()">بازگشت</q-btn>
          </div>

          <AnswerModal :showDialog.sync="showDialog" :form="form" :type="type" :ticket="ticket"
                       :question="question" :answer="answer"></AnswerModal>

        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import moment from 'moment'
import AnswerModal from './AnswerModal'

export default {
  data () {
    return {
      form: {},
      type: 'create',

      showDialog: false,
      ticket: {},
      answer: null,
      question: null
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  methods: {
    isLogin () {
      const app = this

      this.$axios.post(process.env.api + 'api/auth/isLogin/')
        .then(function (response) {
          if (!response.data.login_status) {
            app.$router.push('/login')
          }
          app.$store.commit('shop/setUser', response.data.user)
        })
        .catch(function () {
          app.$router.push('/login')
        })
        .finally(function () {
          app.$q.loading.hide()
          app.CheckIsSupporter()
        })
    },

    CheckIsSupporter () {
      const roles = this.$store.state.shop.user.roles
      if (roles) {
        const result = roles.filter(x => x.role.title === 'supporter')
        if (result.length === 0) {
          window.location.href = '/'
        }
      } else {
        window.location.href = '/'
      }
    },

    CheckIsSupporterOrSuperUser () {
      if (this.$store.state.shop.user.is_superuser) {
        return true
      } else {
        const roles = this.$store.state.shop.user.roles
        if (roles) {
          const result = roles.filter(x => x.role.title === 'supporter')
          if (result.length > 0) {
            return true
          }
        }
      }
      return false
    },

    setAnswerDialog (type = 'create', question = null) {
      if (type !== 'edit') {
        this.NullData()
      }

      this.type = type
      this.question = question

      this.showDialog = true
    },

    ShowCurrentAnswer (question) {
      return this.ticket.answers.filter(x => x.question === question.id)
    },

    ShowImage (url) {
      if (url) {
        return url.replace('http://localhost:8000/', process.env.api)
      }
      return 'https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png'
    },

    NullData () {
      this.form.text = null
      this.question = null
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        progress: true
      })
    },

    EditAnswers (id, question) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/panel/tickets/answers/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.answer = response.data

          app.setAnswerDialog('edit', question)

          app.$q.loading.hide()
        })
    },

    DeleteAnswer (id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید پاسخ مورد نظر حدف شود؟',
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
        app.$axios.delete(process.env.api + 'api/panel/tickets/answers/' + id)
          .then(function () {
            app.showNotif('پاسخ مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetTicket()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    GetTicket () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/tickets/all_users/' + this.$route.params.id)
        .then(function (response) {
          app.ticket = response.data
          app.$q.loading.hide()
        })
    }
  },

  components: {
    AnswerModal
  },

  watch: {
    showDialog (value) {
      if (!value) {
        this.answer = null
        this.question = null
      }
      if (this.form.text) {
        this.GetTicket()
      }
      this.form = {}
    }
  },

  mounted () {
    this.isLogin()
    this.GetTicket()
  }
}
</script>

<style lang="scss">
.faqs-inner {
  margin: 30px 0 40px 0;

  .faq-item {
    background-color: #fff;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;

    .faq-item-inner,
    .faq-answers-inner {
      display: grid;
      grid-template-columns: 60px auto;
    }

    .user-image {
      width: 50px;

      img {
        border-radius: 50%;
        width: 50px;
        height: 50px;
      }

    }

    .user-text {

      h6 {
        font-size: 14px;
        font-weight: 600;
        color: black;
      }

      .text {
        font-size: 14px;
        font-weight: 400;
        color: grey;
        line-height: 26px;
      }

      .user-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 10px;

        .date-content {
          display: flex;
          align-items: center;
          justify-content: flex-start;

          .date,
          .seen {
            font-size: 12px;
            font-weight: 400;
            color: Silver;
            margin-left: 20px;

            .mdi {
              margin-left: 5px;
              font-size: 16px;
              position: relative;
              top: 2px;
            }

          }

          .btn-white {
            background-color: transparent;
            border: none;
            font-size: 12px;
            font-weight: 400;
            color: Silver;
            margin-left: 20px;

            .mdi {
              margin-left: 5px;
              font-size: 16px;
              position: relative;
              top: 2px;
            }

          }

          .like {

            .btn-white {
              color: green;
            }

          }

          .dislike {

            .btn-white {
              margin: 0;
              color: red;
            }

          }
        }

        .answer-content {
          display: flex;
          align-items: center;
          justify-content: center;

          .answer {
            font-size: 12px;
            font-weight: 400;
            color: Silver;
          }

          .see-answer {
            font-size: 13px;
            font-weight: 500;
            margin-right: 20px;

            a {
              color: green;

              .mdi {
                font-size: 14px;
                margin-right: 5px;
                position: relative;
                top: 1px;
              }

            }
          }
        }
      }
    }

    .faq-answers {
      padding: 15px;
      border-radius: 15px;
      margin-top: 20px;
    }

  }
}
</style>
