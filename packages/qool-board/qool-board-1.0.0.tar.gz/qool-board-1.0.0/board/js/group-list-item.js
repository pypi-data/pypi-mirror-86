import {LitElement, customElement, property, html, css} from 'lit-element';

@customElement('group-list-item')
class GroupListItem extends LitElement {
  @property({type: Object}) group = {};
  static styles = css`
    :host {
      display: grid;
      grid-template-columns: 40px 1fr;
      grid-gap: 12px;
    }
    #icon {
      width: 40px;
      height: 40px;
      border-radius: 4px;
      border: 3px solid #0002;
      box-sizing: border-box;
      overflow: hidden;
    }
    #icon img{
      object-fit: cover;
      width: 100%;
      height: 100%;
    }
    #name {
      display: flex;
      align-items: center;
      font-size: 0.85rem;
      font-weight: bold;
      color: #fff;
      height: 40px;
    }
  `;
  render() {
    return html`
      <div id='icon'>
        <img src='api/groups/${this.group._id}/icon' />
      </div>
      <div id='name'>${this.group.name}</div>
    `;
  }
}
