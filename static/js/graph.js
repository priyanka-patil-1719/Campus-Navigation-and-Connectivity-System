/* SVG drawing and playback of Python-generated steps. No graph algorithms here. */
(() => {
  const dataElement = document.querySelector('#graph-data');
  const canvas = document.querySelector('#campus-map');
  if (!dataElement || !canvas) return;
  const data = JSON.parse(dataElement.textContent);
  const NS = 'http://www.w3.org/2000/svg';
  const nodeElements = new Map();
  const edgeElements = [];

  function svgElement(tag, attributes = {}, text) {
    const element = document.createElementNS(NS, tag);
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
    if (text !== undefined) element.textContent = text;
    return element;
  }

  if (!data.nodes.length) {
    canvas.querySelectorAll('.map-region, .compass').forEach(element => element.hidden = true);
    const empty = document.createElement('div');
    empty.className = 'map-empty';
    const heading = document.createElement('h3');
    heading.textContent = 'Your campus starts here';
    const description = document.createElement('p');
    description.textContent = 'Add a location in the Graph Explorer, or load the sample campus to begin.';
    empty.append(heading, description);
    canvas.append(empty);
    return;
  }

  const svg = svgElement('svg', {
    viewBox: `0 0 ${data.width} ${data.height}`, class: 'graph-svg',
    role: 'group', 'aria-label': `Campus graph: ${data.nodes.length} locations, ${data.edges.length} connections`,
  });
  const defs = svgElement('defs');
  ['normal', 'visited'].forEach(kind => {
    const marker = svgElement('marker', {id: `arrow-${kind}`, viewBox: '0 0 10 10',
      refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse'});
    marker.append(svgElement('path', {d: 'M 1 1 L 9 5 L 1 9 z', fill: kind === 'visited' ? '#4b9872' : '#9eb3c7'}));
    defs.append(marker);
  });
  svg.append(defs);
  const lines = svgElement('g', {'aria-hidden': 'true'});
  const weights = svgElement('g', {'aria-hidden': 'true'});
  const nodes = svgElement('g');
  const positions = new Map(data.nodes.map(node => [node.name, node]));

  data.edges.forEach(edge => {
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    const dx = target.x - source.x;
    const dy = target.y - source.y;
    const length = Math.hypot(dx, dy);
    const ux = dx / length;
    const uy = dy / length;
    const reciprocal = data.directed && data.edges.some(other => other.source === edge.target && other.target === edge.source);
    // Drawing geometry only: bend a path if a third building blocks the line.
    const crossesBuilding = data.nodes.some(node => {
      if (node === source || node === target) return false;
      const projection = ((node.x - source.x) * dx + (node.y - source.y) * dy) / (length * length);
      const distance = Math.hypot(node.x - source.x - projection * dx, node.y - source.y - projection * dy);
      return projection > 0.05 && projection < 0.95 && distance < 48;
    });
    // Opposite arrows bend in opposite directions.
    const bend = crossesBuilding ? 140 : (reciprocal ? 25 : 0);
    const x1 = source.x + ux * 32;
    const y1 = source.y + uy * 32;
    const x2 = target.x - ux * 36;
    const y2 = target.y - uy * 36;
    const cx = (x1 + x2) / 2 - uy * bend;
    const cy = (y1 + y2) / 2 + ux * bend;
    const path = svgElement('path', {d: `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`, class: 'graph-edge'});
    if (data.directed) path.setAttribute('marker-end', 'url(#arrow-normal)');
    lines.append(path);
    edgeElements.push({element: path, source: edge.source, target: edge.target});
    if (data.weighted) {
      const x = (x1 + 2 * cx + x2) / 4;
      const y = (y1 + 2 * cy + y2) / 4;
      const label = String(edge.weight);
      const width = label.length * 6.5 + 12;
      weights.append(svgElement('rect', {x: x - width / 2, y: y - 10, width, height: 19, rx: 5, class: 'edge-weight-bg'}));
      weights.append(svgElement('text', {x, y: y + 3.5, class: 'edge-weight'}, label));
    }
  });

  const startSelect = document.querySelector('#start');
  function selectLocation(name) {
    if (!startSelect) return;
    startSelect.value = name;
    startSelect.dispatchEvent(new Event('change'));
  }

  data.nodes.forEach(node => {
    const group = svgElement('g', {class: 'graph-node', transform: `translate(${node.x},${node.y})`});
    group.append(svgElement('title', {}, `${node.number}. ${node.name}`));
    if (canvas.dataset.selectable === 'true') {
      group.setAttribute('role', 'button');
      group.setAttribute('tabindex', '0');
      group.setAttribute('aria-label', `Start traversal at ${node.name}`);
      group.addEventListener('click', () => selectLocation(node.name));
      group.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          selectLocation(node.name);
        }
      });
    }
    group.append(svgElement('rect', {x: -25, y: -23, width: 50, height: 50, rx: 14, class: 'node-shadow'}));
    group.append(svgElement('rect', {x: -25, y: -25, width: 50, height: 50, rx: 14, class: 'node-body'}));
    group.append(svgElement('use', {href: `#i-${node.icon}`, x: -12, y: -12, width: 24, height: 24, class: 'node-icon'}));
    group.append(svgElement('circle', {cx: 23, cy: -22, r: 9, class: 'node-badge'}));
    group.append(svgElement('text', {x: 23, y: -19, class: 'node-id'}, node.number));
    const label = svgElement('text', {x: 0, y: 44, class: 'node-label'});
    const words = node.name.split(' ');
    let line = '';
    const labelLines = [];
    words.forEach(word => {
      if ((line + ' ' + word).trim().length > 20 && line) {
        labelLines.push(line);
        line = word;
      } else line = (line + ' ' + word).trim();
    });
    labelLines.push(line);
    labelLines.forEach((text, index) => {
      const span = svgElement('tspan', {x: 0, dy: index === 0 ? 0 : 15}, text);
      if (text.length > 22) {
        span.setAttribute('textLength', '155');
        span.setAttribute('lengthAdjust', 'spacingAndGlyphs');
      }
      label.append(span);
    });
    group.append(label);
    nodes.append(group);
    nodeElements.set(node.name, group);
  });
  svg.append(lines, weights, nodes);
  canvas.append(svg);
  startSelect?.addEventListener('change', () => {
    nodeElements.forEach((element, name) => {
      const selected = name === startSelect.value;
      element.classList.toggle('selected', selected);
      element.setAttribute('aria-pressed', String(selected));
    });
  });
  startSelect?.dispatchEvent(new Event('change'));

  const resultElement = document.querySelector('#traversal-data');
  if (!resultElement) return;
  const result = JSON.parse(resultElement.textContent);
  const playButton = document.querySelector('#play-pause');
  const nextButton = document.querySelector('#next-step');
  const restartButton = document.querySelector('#restart');
  const speed = document.querySelector('#speed');
  const frontier = document.querySelector('#frontier');
  const description = document.querySelector('#step-description');
  const orderItems = document.querySelectorAll('[data-visit]');
  document.querySelector('#playback-controls').hidden = false;
  document.querySelector('#working-state').hidden = false;
  let index = -1;
  let timer = null;
  let playing = false;

  function paintStep() {
    const step = result.steps[index];
    nodeElements.forEach((element, name) => {
      element.classList.toggle('visited', Boolean(step?.visited.includes(name)));
      element.classList.toggle('current', step?.current === name);
      element.classList.remove('selected');
    });
    orderItems.forEach(item => {
      item.classList.toggle('visited', Boolean(step?.visited.includes(item.dataset.visit)));
      item.classList.toggle('current', step?.current === item.dataset.visit);
      if (step?.current === item.dataset.visit) item.setAttribute('aria-current', 'step');
      else item.removeAttribute('aria-current');
    });
    edgeElements.forEach(edge => {
      const traversed = Boolean(step?.tree_edges.some(([from, to]) =>
        (from === edge.source && to === edge.target) ||
        (!data.directed && from === edge.target && to === edge.source))) && Boolean(step?.visited.includes(edge.target)) && Boolean(step?.visited.includes(edge.source));
      edge.element.classList.toggle('traversed', traversed);
      if (data.directed) edge.element.setAttribute('marker-end', `url(#arrow-${traversed ? 'visited' : 'normal'})`);
    });
    frontier.replaceChildren();
    if (step) {
      const complete = index === result.steps.length - 1;
      description.textContent = `${complete ? 'Final visit' : 'Visiting'}: ${step.current} · ${result.algorithm === 'BFS' ? 'Level' : 'Depth'} ${step.depth}${complete ? `. ${result.order.length} of ${data.nodes.length} locations reached.` : ''}`;
      step.frontier.forEach(name => {
        const chip = document.createElement('span');
        chip.textContent = name;
        frontier.append(chip);
      });
      if (!step.frontier.length) {
        const empty = document.createElement('span');
        empty.className = 'empty-frontier';
        empty.textContent = 'Queue empty';
        frontier.append(empty);
      }
    } else description.textContent = 'Press Play or Next step to begin.';
    document.querySelector('#step-counter').textContent = `${index + 1} / ${result.steps.length} steps`;
    document.querySelector('#traversal-progress').style.width = `${(index + 1) / result.steps.length * 100}%`;
    nextButton.disabled = index >= result.steps.length - 1;
  }

  function pause() {
    playing = false;
    window.clearTimeout(timer);
    playButton.textContent = index === result.steps.length - 1 ? 'Replay' : 'Play';
  }
  function advance() {
    if (index < result.steps.length - 1) index += 1;
    paintStep();
    if (index === result.steps.length - 1) pause();
    else if (playing) timer = window.setTimeout(advance, Number(speed.value));
  }
  function play() {
    if (index === result.steps.length - 1) index = -1;
    playing = true;
    playButton.textContent = 'Pause';
    advance();
  }
  playButton.addEventListener('click', () => playing ? pause() : play());
  nextButton.addEventListener('click', () => { pause(); advance(); });
  restartButton.addEventListener('click', () => { pause(); index = -1; playButton.textContent = 'Play'; paintStep(); });
  speed.addEventListener('change', () => {
    if (playing) { window.clearTimeout(timer); timer = window.setTimeout(advance, Number(speed.value)); }
  });
  window.addEventListener('pagehide', pause);
  paintStep();
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) play();
})();
