import {LitElement, customElement, property, html, css} from 'lit-element';

@customElement('board-app')
class BoardApp extends LitElement {
  @property({type: Array}) general = [];
  @property({type: Array}) groups = [];
  @property({type: Array}) others = [];
  @property({type: Array}) boards = [];
  static styles = css`
    :host{
      display: block;
      height: 100vh;
      width: 100%;
      box-sizing:border-box;
      padding-left: 240px;
      overflow: hidden;
    }
    ::-webkit-scrollbar {
      height: 8px;
    }
    ::-webkit-scrollbar-track {
      background: #0000;
    }
    ::-webkit-scrollbar-thumb {
      background-color: #0004;
      border-radius: 4px;
    }
    #header{
      position: absolute;
      height: 100vh;
      width: 240px;
      top: 0;
      box-sizing: border-box;
      background: #333c5e;
      padding: 20px;
      left: 0;
      user-select: none;
      box-shadow: 0 0 8px #0004;
      z-index: 10;
    }
    #header label{
      display: block;
      position: relative;
    }
    #header input[type='checkbox'] {
      display: none;
    }
    #header input[type='checkbox'] ~ board-form {
      display: none;
    }
    #header input[type='checkbox']:checked ~ board-form {
      display: block;
      top: 0;
      position: absolute;
      z-index: 10;
      left: 54px;
    }
    #header .section_header h3{
      font-size: 0.9rem;
      margin: 0;
      height:40px;
      line-height: 40px;
      color: #fff;
    }
    .split,.group-header{
      display: grid;
      grid-template-columns: 1fr 24px;
      align-items: center;
    }
    .boards{
      padding-top: 8px;
      padding-left: 8px;
      padding-bottom: 12px;
    }
    #main {
      box-sizing: border-box;
      padding: 24px;
      height: 100vh;
      width: 100%;
      overflow-y: hidden;
      overflow-x: scroll;
      display: flex;
    }
  `;
  async connectedCallback() {
    super.connectedCallback();
    this.general = await fetch('api/boards').then(res => res.json());
    this.groups = await fetch('api/users/'+window.user._id).then(res => res.json()).then(async res => {
      return await Promise.all(res.parents.map(async group => {
        group.boards = await fetch('api/groups/'+group._id+'/boards').then(res => res.json());
        return group;
      }));
    });
    this.others = await fetch('api/users/'+window.user._id+'/boards').then(res => res.json());
    JSON.parse(localStorage.getItem('columns')).forEach(b => {
      this.addColumn(b);
    });
  }
  async addColumn(board_id) {
    const board = await fetch('api/boards/'+board_id).then(res => res.json());
    this.boards.push(board);
    const board_arr = this.boards.map(b => b._id);
    localStorage.setItem('columns', JSON.stringify(board_arr))
    this.requestUpdate();
  }
  render() {
    return html`
      <div id='header'>
        <div>
          <div class='section_header split'>
            <h3>全体</h3>
            <div>
              <board-create-button .group=${{_id: ''}} .addColumn=${this.addColumn}></board-create-button>
            </div>
          </div>
          <div class='section_content'>
            <div class='boards'>
              ${this.general.map(b => html`
                <board-list-item .board=${b} @click=${()=>this.addColumn(b._id)}></board-list-item>
              `)}
            </div>
          </div>
        </div>
        <div>
          <div class='section_header'>
            <h3>所属グループ</h3>
          </div>
          <div class='section_content'>
          ${this.groups.map(g => html`
            <div class='group'>
              <div class='group-header'>
                <group-list-item .group=${g} ></group-list-item>
                <div>
                  <board-create-button .group=${g} .addColumn=${this.addColumn}></board-create-button>
                </div>
              </div>
              <div class='boards'>
                ${g.boards.map(b => html`
                  <board-list-item .board=${b} @click=${()=>this.addColumn(b._id)}></board-list-item>
                `)}
              </div>
            </div>
          `)}
          </div>
        </div>
      </div>
      <div id='container'>
        <div id='main'>
          ${this.boards.map(board => html`
            <board-page .board=${board}></board-page>
          `)}
        </div>
      </div>
    `;
  }
}
