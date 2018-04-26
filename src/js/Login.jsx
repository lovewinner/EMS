import React from 'react'
import ReactDOM from 'react-dom'
import Loading from "./Components/Loading/Loading";
import BannerImage from '../images/grid_seamless.png'

import '../css/materialize.min'
import '../css/fonts'

class Login extends React.Component {
    constructor() {
        super()
        this.state = {
            settings: {
                login_url: '/login/authentication',
                username_valid: false,
                password_valid: false,
                loading: false,
                action: 'LOGIN'
            },
            form: {
                username: '',
                password: ''
            }
        }
    }

    formSubmit = (e) => {
        e.preventDefault()
        const { username, password, action } = e.target;

        this.setState({
            settings: {...this.state.settings, loading: true, username_valid: false, password_valid: false}
        })
        setTimeout(() => {
            this.setState({
                settings: { ...this.state.settings, loading: false, username_valid: true, password_valid: true }
            })
            Materialize.toast('账号或密码错误，请重新登录！', 4000)
        }, 3000);
        console.log({
            username: username.value,
            password: password.value,
            action: action.value
        })
    }

    render() {
        
        const { settings, form } = this.state
        const { username, password } = this.state.form
        const { username_valid, password_valid, action } = this.state.settings

        const cardImageStyle = {
            marginBottom: "1em",
            marginLeft: "-.75em",
            marginRight: "-.75em",
            height: "13.5em",
            backgroundImage: `url(${BannerImage})`,
            backgroundPosition: 'right 1px top -4px;',
            backgroundRepeat: 'repeat',
            backgroundSize: "19px",
        }

        const ImageStyle = {

        }

        const class_names_submit = (() => {
            let classNmaes = 'btn waves-effect waves-light blue accent-2 right '
            if (!username_valid || !password_valid) {
                classNmaes += 'disabled'
            }
            return classNmaes
        })()

        return (
            <div class="row">
                <div class="card middle col s4 offset-s4" style={{marginTop: "10%"}}>
                    <div class="card-image" style={cardImageStyle}>
                        <div class="card-title" style={{color: '#565656'}}>
                            <h4>登陆</h4>
                            <h5 style={{fontSize: ".83em"}}>动力工程系试验管理平台</h5>
                        </div>
                    </div>
                    <form id="formValidate" class="col s12 right-alert" onSubmit={this.formSubmit.bind(this)} style={{padding:"1em 0 0 0"}}>
                        <div class="raw">
                            <div class="input-field col s12">
                                <input id="username"
                                    class="validate"
                                    type="text"
                                    name="username"
                                    placeholder="请输入12位的学号"
                                    value={username}
                                    onChange={(e) => {
                                        this.setState({
                                            settings: {...settings, username_valid: e.target.checkValidity()},
                                            form: {...form, username: e.target.value } })
                                    }}
                                    required={true}
                                    maxLength="12"
                                    minLength="7"
                                />
                                <label for="student_numebr" data-error="请输入正确的12位学号">学号</label>
                            </div>
                        </div>
                        <div class="raw">
                            <div class="input-field col s12">
                                <input id="password"
                                    class="validate"
                                    type="password"
                                    name="password"
                                    required
                                    value={password}
                                    onChange={(e) => {
                                        this.setState({
                                            settings: { ...settings, password_valid: e.target.checkValidity() },
                                            form: { ...form, password: e.target.value }
                                        })
                                    }}
                                    onBlur={(e) => {
                                        this.setState({
                                            settings: { ...settings, password_valid: e.target.checkValidity() }
                                        })
                                    }}
                                />
                                <label for="password" data-error="密码不能为空">密码</label>
                            </div>
                        </div>
                        <div class="row">
                            <div class="input-field col s12">
                                <button class={class_names_submit} type="submit" name="action" value={action}>登陆
                                    <i class="material-icons right">send</i>
                                </button>
                                <Loading loading={this.state.settings.loading} size="small"/>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    }    
}

const login = document.getElementById('login')

ReactDOM.render(<Login />, login)