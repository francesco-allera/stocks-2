function avgLastN(arrInput, num, idx, date, arrOutput) {
   let counter = idx < num ? (idx + 1) : num;
   let sum = 0;

   for (let i = 0; i < counter; i++)
      sum += arrInput[idx - i].close;

   arrOutput.push({
      x: date,
      y: sum / counter
   });
}

for (y in stocks) {
   document.querySelector('#stocks').innerHTML += '<option value="' + y + '">' + y.replace(/_/g, ' ') + '</option>';
}

const id = 'chartContainer';
const arrays = { closes: [], avgs: [] };
const periods = [25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000];
let data, stock;

periods.forEach(el => arrays['avgLast' + el] = []);

document.querySelector('#stocks').addEventListener('change', function() {
   function toggleDataSeries(e) {
      if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible)
         e.dataSeries.visible = false;
      else
         e.dataSeries.visible = true;

      chart.render();
   }

   if (document.querySelector('#' + id))
      document.querySelector('#' + id).remove();

   const canvas = document.createElement('div');
   canvas.setAttribute('id', id);
   document.querySelector('#app').appendChild(canvas);

   for (x in arrays)
      arrays[x] = [];

   data = [];
   stock = stocks[this.value];

   let sumCloses = 0;

   stock.forEach((el, i, arr) => {
      const dmy = new Date(el.yy, el.mm - 1, el.dd);
      sumCloses += el.close;

      arrays.closes.push({
         x: dmy,
         y: el.close
      });

      arrays.avgs.push({
         x: dmy,
         y: sumCloses / (i + 1)
      });

      periods.forEach(item => avgLastN(arr, item, i, dmy, arrays['avgLast' + item]));
   });

   for (arr in arrays) {
      data.push({
         type: 'line',
         showInLegend: true,
         name: arr,
         dataPoints: arrays[arr]
      });
   }

   const chart = new CanvasJS.Chart(id, {
      animationEnabled: true,
      axisX: { valueFormatString: "MM YY" },
      legend:{
         cursor: "pointer",
         fontSize: 12,
         itemclick: toggleDataSeries
      },
      toolTip:{ shared: true },
      data
   });

   chart.render();
});
