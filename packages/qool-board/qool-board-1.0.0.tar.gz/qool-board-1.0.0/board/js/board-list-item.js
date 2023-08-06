import {LitElement, customElement, property, html, css} from 'lit-element';

@customElement('board-list-item')
class BoardListItem extends LitElement {
  @property({type: Object}) board = {};
  static styles = css`
    :host {
      display: block;
      padding: 0 8px;
    }
    :host(:hover){
      background: #0002;
    }
    #name {
      display: flex;
      align-items: center;
      font-size: 0.9rem;
      color: #fff;
      height: 32px;
      font-weight: bold;
    }
  `;
  render() {
    return html`
      <div id='name'>${this.board.subject}</div>
    `;
  }
}
