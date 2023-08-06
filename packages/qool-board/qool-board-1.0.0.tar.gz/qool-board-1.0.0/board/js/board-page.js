import {LitElement, html, css, property, customElement} from 'lit-element';
import Compressor from 'compressorjs';
import marked from 'marked';

const fix = f => f = f((...x) => f(...x));

class Post {
  constructor(id, board, user, content, posted, page) {
    this._id = id;
    this.boardId = board;
    this.user = user;
    this.posted = posted;
    this.replyto = null;
    this.replied = [];
    this.parseContent(content, page);
  }
  formatPosted() {
    let posted = new Date(this.posted);
    let now = new Date();
    posted = (
      (posted.getFullYear() != now.getFullYear())
        ? (posted.getFullYear() + '/')
        : ''
      ) + posted.getMonth() + '/' + posted.getDate() + ' ' + ('00' + posted.getHours()).slice(-2) + ':' + ('00' + posted.getMinutes()).slice(-2);
    return posted;
  }
  parseContent(txt, page) {
    let content = new Array();
    let values = new Array();
    txt = txt.replace(/^>>([\d]+)(.*)/,(whole, link, text) => {
      this.replyto = Number(link);
      content.push('<span class="response_anker" @click=');
      content.push('>&gt;&gt;'+this.replyto+'</span> ');
      values.push(() => {
        page.scroll('#post-'+this.replyto);
      })
      return text;
    });
    txt = marked.parseInline(txt.trim());
    content.push(txt);
    this.content = html(content, ...values);
  }
  addReplied(post) {
    this.replied.push(post);
  }
}

@customElement('board-page')
class BoardPage extends LitElement {
  @property({type: Object}) board;
  @property({type: String}) subject = "";
  @property({type: Object}) posts = {};
  @property({type: Object}) thread = null;
  @property({type: Boolean}) hideReply = false;
  async connectedCallback() {
    super.connectedCallback();
    this.lastTime = new Date(0);
    await this._update()
    setTimeout(() => {
      const elem = this.shadowRoot.querySelector('#main');
      elem.scrollTop = elem.scrollHeight;
    }, 500)
    this.interval = setInterval(() => this._update(), 5000);
  }
  disconnectedCallback() {
    clearInterval(this.interval);
  }
  async _update() {
    const data = await fetch('api/boards/'+this.board._id + '?since=' + this.lastTime.toISOString()).then(res => res.json());
    this.subject = data.subject;
    for (let post of data.posts) {
      if (!Object.keys(this.posts).some(k => {
        if (this.posts[k]._id == post._id) {
          this.posts[k] = post;
          return true;
        }
        return false;
      })) {
        const post_ = new Post(post._id, this.board._id, post.user, post.content, post.posted, this);
        this.posts[post_._id] = post_;
        if(post_.replyto != null) {
          post_.replytoObj = this.posts[post_.replyto];
          this.posts[post_.replyto].addReplied(post_);
        }
      }
    }
    this.lastTime = new Date();
    this.requestUpdate();
  }
  static styles = css`
    :host {
      height: 100%;
      display: grid;
      margin-right: 8px;
      grid-template-columns: 360px auto;
      grid-template-rows: 1fr;
      box-shadow: 0 0 8px #0003;
    }
    #wrapper {
      width: 360px;
      background: #fff;
      height: 100%;
      display: grid;
      grid-template-rows: 48px 1fr auto;
      overflow-y: hidden;
      position: relative;
    }
    #header{
      display: grid;
      grid-template-columns: 12px 1fr auto;
      grid-gap: 16px;
      align-items: center;
      margin: 0;
      height: 32px;
      line-height: 32px;
      padding: 8px 16px;
      background: #333c5e;
      color: #fff;
    }
    .close-button{
      display: block;
      position: relative;
      width: 12px;
      height: 12px;
      padding: 0;
    }
    .close-button::before,
    .close-button::after{
      content: '';
      display: block;
      position: absolute;
      top: 5px;
      left: 0px;
      width: 12px;
      height: 2px;
      transform-origin: center;
      background: #fff;
      transform: rotate(45deg);
    }
    .close-button::after{
      transform: rotate(135deg);
    }
    #header h3{
      margin: 0;
      font-size: 1rem;
    }
    #hide_button{
      font-size: 0.8rem;
    }
    #main {
      padding: 8px;
      position: relative;
      overflow-y: scroll;
      overflow-x: hidden;
    }
    ::-webkit-scrollbar {
      width: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #0000;
    }
    ::-webkit-scrollbar-thumb {
      background-color: #0004;
      border-radius: 4px;
    }
    #hide {
      display: none;
    }
    #hide:checked ~ #main post-item[replyto] {
      display: none;
    }
    #thread-wrapper{
      width: 0;
      overflow: hidden;
    }
    #thread-wrapper.open{
      background: #fff7;
      min-width: 240px;
      padding: 8px 0 8px 8px;
      overflow-y: scroll;
    }
    #thread-wrapper #thread-header {
      height: 32px;
      padding: 0 8px;
      box-sizing: border-box;
      align-items: center;
      display: flex;
    }
    #thread-close{
      height: 8px;
      width: 8px;
      border-top: 2px solid #777;
      border-left: 2px solid #777;
      transform-origin: center;
      box-sizing: border-box;
      transform: rotate(-45deg);
    }
    #thread-wrapper post-item {
      width: 100%;
    }
    #main-post-form {
      border-top: 1px solid #aaa;
    }
    #members {
      height: 40px;
      padding: 4px;
      box-sizing: border-box;
      width: 100%;
      display: grid;
      grid-gap: 16px;
      grid-template-columns: auto 1fr;
    }
    .user-icon, .group-icon{
      height: 32px;
      width: 32px;
      box-sizing: border-box;
      border: 3px solid #0002;
      object-fit: cover;
    }
    .user-icon {
      border-radius: 16px;
    }
    .group-icon {
      border-radius: 2px;
    }
  `;
  scroll(to) {
    const elem = this.shadowRoot.querySelector(to);
    const main = this.shadowRoot.querySelector('#main');
    console.log(elem.scrollTop, main.scrollTop);
    main.scrollTop = elem.offsetTop;
  }
  threadView(post) {
    if(this.thread == null || post._id != this.thread._id){
      this.thread = post
    }else{
      this.thread = null;
    }
  }
  close() {
    this.parentNode.removeChild(this);
  }
  render() {
    return html`
      <div id='wrapper'>
        <input type='checkbox' id='hide' />
        <div id='header'>
          <div class='close-button' @click=${e => this.close()}></div>
          <h3>${this.board.group!=null ? this.board.group.name + ' / ' : null}${this.subject}</h3>
          <label for='hide' id='hide_button'>
             リプライを隠す
          </label>
        </div>
        <div id='main'>
          ${Object.keys(this.posts).sort((a,b) => Number(a)>Number(b)?1:-1).map(k => {
            let post = this.posts[k];
            return html`
              <post-item
                id='post-${post._id}'
                .replyto=${post.replyto}
                .post=${post}
                .anker=${to=>this.scroll(to)}
                .thread=${() => this.threadView(post)}
                .afterreply=${()=> this._update()}
              ></post-item>
            `
          })}
        </div>
        <post-form
          id='main-post-form'
          .afterpost=${()=> this._update()}
          board=${this.board._id}
          ?board-editable=${false}
        ></post-form>
      </div>
      <div id='thread-wrapper' class=${this.thread!=null?'open':''}>
        <div id='thread-header'>
          <div id='thread-close' @click=${() => this.thread=null}></div>
        </div>
        ${this.thread != null ? [
          this.thread.replyto != null ? fix(ren => {
            return post => {
              let arr = [];
              let elem = html`
                <post-item
                  id='post-${post._id}'
                  .post=${post}
                  .anker=${to=>this.scroll(to)}
                  .thread=${() => this.threadView(post)}
                  .afterreply=${()=> this._update()}
                ></post-item>
              `;
              if(post.replyto != null) arr = arr.concat(ren(post.replytoObj));
              arr.push(elem);
              return arr;
            }
          })(this.thread.replytoObj) : html``,
          html`
          <post-item
            id='post-${this.thread._id}'
            .post=${this.thread}
            .anker=${to=>this.scroll(to)}
            .thread=${() => this.threadView(this.thread)}
            .afterreply=${()=> this._update()}
          >
          ${fix(ren => {
            return post => {
              return html`
                ${post.replied.map(post => html`
                  <post-item
                    id='post-${post._id}'
                    .post=${post}
                    .anker=${to=>this.scroll(to)}
                    .thread=${() => this.threadView(post)}
                    .afterreply=${()=> this._update()}
                  >
                    ${ren(post)}
                  </post-item>
                `)}
              `;
            }
          })(this.thread)}
          </post-item>`
        ] : html``}
        <post-form
          .afterpost=${()=> this._update()}
          .content=${this.thread!=null ? '>>'+this.thread._id+' ' : ''}
          board=${this.board._id}
          ?board-editable=${false}
        ></post-form>
      </div>
    `;
  }
}
