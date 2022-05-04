<script>
  import {onMount} from 'svelte';
  import {createTask} from '../tasks.js';
  // import {createLayerSimple, getLayer} from '../layers.js';
  import CMTask from './CMTask.svelte';
  import {areaSelectionLayerStore, selectedLayerStore, tasksStore, datasetsStore} from '../stores.js';
  import {getDataset} from '../datasets.js';
  import 'brutusin-json-forms';
  import AreaSelection from './AreaSelection.svelte';
  let activeMainTab = 'consultation';

  const BrutusinForms = brutusin['json-forms'];

  export let cm;
  let isDisabled = true;
  let tasks = [];
  let formElement = null;
  let form = undefined;
  let callCMTooltip = '';
  let isCollapsed = false;
  let layersText = null;
  let layersLinkText = null;
  let layersLinkDatasetId = null;
  let layersDetails = null;
  // let layersDetailsDisplayed = false;
  // let testhidden = false;


  onMount(() => {
    form = BrutusinForms.create(cm.schema);
    form.render(formElement);
  });





  function toggleCollapse() {
    isCollapsed = !isCollapsed;
  }


  // function toggleLayersDetails() {
  //  layersDetailsDisplayed = !layersDetailsDisplayed;
  // }


  // async function onDatasetClicked(datasetId, variable) {
  //  const dataset = getDataset(datasetId);

  //  let timePeriod = null;

  //  if (variable == null) {
  //    if (dataset.info.default_parameters.variable !== undefined) {
  //      variable = dataset.info.default_parameters.variable;
  //    } else if (dataset.info.variables.length > 0) {
  //      variable = dataset.info.variables[0];
  //    }
  //  }

  //  if (dataset.info.time_periods.length > 0) {
  //    timePeriod = dataset.info.time_periods[0];
  //  }

  //  await createLayerSimple(dataset.ds_id, variable, timePeriod);
  // }
</script>


<style>
  .tasks {
    margin-top: 10px;
    position: relative;
  }

  .open_menu {
    display: inline-block;
    height: 25px;
    width: 25px;
    background: url('../images/menu-close-icon.png');
    background-size : 100%;
  }

  .cm_run {
    vertical-align: middle;
    display: inline-block;
  }

  .close_menu {
    display: inline-block;
    height: 25px;
    width: 25px;
    background: url('../images/menu-open-icon.png');
    background-size : 100%;
  }

  .cm_params {
    margin-top: 10px;
    overflow-x: auto;
  }

  .cm_container {
    background-color : #6da8d7;
    margin-top: 8px;
    margin-bottom: 8px;
    padding : 8px;
    border-radius: 4px;
    width: inherit;
  }

  .cm_container_test {
    background-color : white;
    margin-top: 8px;
    margin-bottom: 8px;
    padding : 8px;
    border-radius: 4px;
    width: inherit;
  }
  .cm_container.disabled {
    background-color: darkgray;
  }

  /*.cm_info {*/
  /*  font-style: italic;*/
  /*  color: rgb(69, 69, 101);*/
  /*  margin-top: 4px;*/
  /*}*/

  /*.cm_info span {*/
  /*  cursor: pointer;*/
  /*  color: rgb(0,100,200);*/
  /*}*/

  /*.cm_wiki {*/
  /*  font-style: italic;*/
  /*  color: rgb(69, 69, 101);*/
  /*  margin-top: 4px;*/
  /*}*/

  /*.cm_wiki a {*/
  /*  cursor: pointer;*/
  /*  color: rgb(0,100,200);*/
  /*}*/

  h3 {
    margin: 0;
  }

  /*.layers-details {*/
  /*  position: fixed;*/
  /*  background-color: lightgray;*/
  /*  border: 1px solid #333333;*/
  /*  border-radius: 4px;*/
  /*  padding: 6px;*/
  /*  margin-left: 20px;*/
  /*  z-index: 1000;*/
  /*}*/

  /*.layers-details p {*/
  /*  margin-top: 0;*/
  /*}*/

  /*.layers-details ul {*/
  /*  margin-bottom: 0;*/
  /*  padding-left: 20px;*/
  /*}*/

  span.main_tab {
    border: 1px solid black;
    padding: 4px;
    margin-left: 0;
    margin-right: 0;
    background-color: #f7f7f7;
    cursor: pointer;
    border-radius: 4px;
  }
  span.main_tab.selected {
    border-bottom: 5px solid white;
    font-weight: bold;
    background-color: white;
    border-radius: 6px;
  }

  /*span.main_tab.last {*/
  /*  margin-right: 24px;*/
  /*}*/
</style>


<div class="cm_container" class:disabled={isDisabled}>


  <div hidden="{isCollapsed}">
    <!--{#if layersLinkDatasetId}-->
    <!--  <div class="cm_info">-->
    <!--    {layersText}-->
    <!--    {#if layersLinkText}-->
    <!--      <span title="Add the dataset as a layer"-->
    <!--            on:click={() => onDatasetClicked(layersLinkDatasetId, null)}>-->
    <!--        {layersLinkText}-->
    <!--      </span>-->
    <!--    {/if}-->
    <!--  </div>-->
    <!--{:else}-->
    <!--  <div class="cm_info">-->
    <!--    {layersText}-->
    <!--    {#if layersLinkText}-->
    <!--      <span title="Display the list of supported datasets" on:click={toggleLayersDetails}>{layersLinkText}</span>-->
    <!--    {/if}-->
    <!--    {#if layersDetailsDisplayed && layersDetails}-->
    <!--      <div class="layers-details" on:click={toggleLayersDetails} on:mouseleave={toggleLayersDetails}>-->
    <!--        <p>This CM requires one of the following datasets:</p>-->
    <!--        <ul>-->
    <!--          {#each layersDetails as details}-->
    <!--            <li>-->
    <!--              {#if details.variables}-->
    <!--                {details.dataset_title}-->
    <!--                <ul>-->
    <!--                {#each details.variables as variable}-->
    <!--                  <li>-->
    <!--                    <span on:click={() => onDatasetClicked(details.dataset_id, variable)}>{variable}</span>-->
    <!--                  </li>-->
    <!--                {/each}-->
    <!--                </ul>-->
    <!--              {:else}-->
    <!--                <span on:click={() => onDatasetClicked(details.dataset_id, null)}>{details.dataset_title}</span>-->
    <!--              {/if}-->
    <!--            </li>-->
    <!--          {/each}-->
    <!--        </ul>-->
    <!--      </div>-->
    <!--    {/if}-->
    <!--  </div>-->
    <!--{/if}-->

    <!--<div class="cm_wiki">-->
    <!--  <i>-->
    <!--    For more information about the CM,-->
    <!--    see <a href="{cm.wiki}" target="_blank">the wiki pages</a>.-->
    <!--  </i>-->
    <!--</div>-->

<!--    Start Tabs-->
    <span class="main_tab" class:selected={activeMainTab === 'consultation'} on:click={() => (activeMainTab = 'consultation')}>Consultation</span>
    <span class="main_tab" class:selected={activeMainTab === 'analysis'} on:click={() => (activeMainTab = 'analysis')}>Analyse</span>
    {#if activeMainTab === 'consultation'}
    <div class="cm_container_test">
      <p>Mode consultation activé</p>
<!--      <div hidden="testhidden"> -->
        <div class="cm_params" bind:this={formElement}></div>
      </div>
<!--    </div> -->
    {:else if activeMainTab === 'analysis'}
      <div class="cm_container_test">
        <AreaSelection />
      </div>
      <div class="tasks">
        {#each [...tasks].reverse() as task (task.id)}
          {#if (task.cm.name === cm.name) && !task.hidden}
            <CMTask task={task} />
          {/if}
        {/each}
      </div>
    {/if}
<!--    End Tabs-->
  </div>
</div>
