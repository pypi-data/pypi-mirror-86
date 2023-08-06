import {LitElement, html, css, property, customElement} from 'lit-element';


@customElement('post-item')
class PostItem extends LitElement {
  @property({type: Object}) post;
  @property({type: Number, attribute: 'replyto', reflect: true}) replyto;
  @property({type: Function}) anker;
  @property({type: Function}) thread;
  @property({type: Function}) afterreply;
  static styles = css`
    :host{
      display: block;
    }
    #wrapper{
      width: 100%;
      box-sizing: border-box;
      padding: 8px;
    }
    #index {
      color: #555;
      font-size: 0.75rem;
    }
    #container {
      display: grid;
      grid-template-columns: 40px 1fr; 
      grid-gap: 16px;
    }
    #icon {
      width: 40px;
      height: 40px;
    }
    #icon img{
      width: 40px;
      height: 40px;
      border-radius: 20px;
      object-fit: cover;
    }
    #header {
      display: flex;
      justify-content: space-between;
    }
    #name {
      font-weight: bold;
      font-size: 0.9rem;
    }
    #datetime{
      font-size: 0.8rem;
      color: #777;
    }
    #content {
      margin: 0;
      padding: 8px 0;
      font-size: 1rem;
    }
    #content img {
      max-width: 100%;
      height: auto;
      box-sizing: border-box;
      border: 3px solid #0002;
      border-radius: 6px;
    }
    blockquote {
      margin: 0;
      margin-left: 8px;
      padding-left: 8px;
      border-left: 2px solid #ccc;
    }
    #footer svg{
      height: 12px;
      width: 12px;
      display: block;
      margin-right: 4px;
    }
    #footer {
      color: #777;
      fill: #777;
      font-size: 0.8rem;
      display: flex;
      align-items: center;
      height: 24px;
      margin-top: 8px;
    }
    #footer button,
    #footer label {
      height: 24px;
      line-height: 24px;
      border-radius: 12px;
      background: #0001;
      color: #777;
      fill: #777;
      font-size: 0.6rem;
      padding: 0 12px;
      margin-right: 8px;
    }
    #footer button:hover,
    #footer label:hover {
      background: #0002;
    }
    #footer button:active,
    #footer label:active {
      background: #0004;
    }
    #children {
      width: calc(100% - 8px);
      margin-left: 8px;
      position: relative;
    }
    #children::before {
      content: '';
      display: block;
      height: 100%;
      background: #0004;
      position: absolute;
      width: 2px;
      top: 0;
      left: -2px;
    }
    #comments {
      border: none;
      display: inline-grid;
      grid-template-columns: 12px auto;
      grid-gap: 4px;
      background: none;
      align-items: center;
    }
    #repling {
      display: none;
    }
    #reply-form{
      display: none;
    }
    #repling:checked ~ #reply-form{
      display: block;
    }
    .response_anker {
      color: #333c5e;
      font-weight: bold;
    }
  `;
  render() {
    return html`
      <div id='wrapper'>
        <div id='container'>
          <div id='icon'>
            <img src='${this.post.user.icon}' />
          </div>
          <div id='main'>
            <div id='header'>
              <div id='name'>
                <span id='index'>
                  #${this.post._id}
                </span>
                ${this.post.user.screen_name}
              </div>
              <div id='datetime'>
                ${this.post.formatPosted()}
              </div>
            </div>
            <div id='content'>${this.post.content}</div>
            <div id='footer'>
              <button id='comments' @click=${() => this.thread() }>
                <svg>
                  <use xlink:href='static/spritesheet.svg#icon-bubble'></use>
                </svg>
                ${this.post.replied.length}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div id='children'>
        <slot></slot>
      </div>
    `;
  }
}
