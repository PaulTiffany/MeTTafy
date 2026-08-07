(() => {
  "use strict";

  const player = document.querySelector("[data-strategy-player]");
  if (!player) return;

  const steps = Array.from(player.querySelectorAll("[data-step]"));
  const arrows = Array.from(player.querySelectorAll("[data-arrow]"));
  const status = player.querySelector("[data-status]");
  const playButton = player.querySelector('[data-action="play"]');
  const prevButton = player.querySelector('[data-action="prev"]');
  const nextButton = player.querySelector('[data-action="next"]');
  const resetButton = player.querySelector('[data-action="reset"]');

  let index = 0;
  let timer = null;

  function render() {
    steps.forEach((step, i) => {
      step.classList.toggle("active", i === index);
      step.classList.toggle("done", i < index);
      step.setAttribute("aria-current", i === index ? "step" : "false");
    });

    arrows.forEach((arrow, i) => {
      arrow.classList.toggle("active", index > 0 && i === index - 1);
      arrow.classList.toggle("done", i < index - 1);
    });

    const name = steps[index]?.dataset.label || `step ${index + 1}`;
    status.textContent = `Step ${index + 1} of ${steps.length}: ${name}`;
    prevButton.disabled = index === 0;
    nextButton.disabled = index === steps.length - 1;
  }

  function stop() {
    if (timer !== null) {
      window.clearInterval(timer);
      timer = null;
    }
    playButton.textContent = "Play";
    playButton.setAttribute("aria-pressed", "false");
  }

  function next() {
    if (index >= steps.length - 1) {
      stop();
      return;
    }
    index += 1;
    render();
  }

  function prev() {
    stop();
    if (index > 0) index -= 1;
    render();
  }

  function reset() {
    stop();
    index = 0;
    render();
  }

  function play() {
    if (timer !== null) {
      stop();
      return;
    }
    if (index === steps.length - 1) index = 0;
    render();
    playButton.textContent = "Pause";
    playButton.setAttribute("aria-pressed", "true");
    timer = window.setInterval(next, 950);
  }

  playButton.addEventListener("click", play);
  prevButton.addEventListener("click", prev);
  nextButton.addEventListener("click", () => {
    stop();
    next();
  });
  resetButton.addEventListener("click", reset);

  render();
})();
