// Elements
const videoContainer = document.querySelector(".video-container");
const videoElements = document.querySelectorAll("video");

// If in view, play video and unmute
const observer = new IntersectionObserver(
	(entries) => {
		entries.forEach((entry) => {
			const video = entry.target;
			if (entry.isIntersecting) {
				video.play();
				video.muted = false;
			} else {
				video.pause();
				video.muted = true;
			}
		});
	},
	{ threshold: 0.5 }
);

// Get the list of video files from the server
fetch("/get_videos")
	.then((response) => response.json())
	.then((videos) => {
		// Create a new video item for each video
		// Preload the video, mute it, and add event listeners
		videos.forEach((video) => {
			const videoItem = document.createElement("section");
			videoItem.classList.add("video-item");

			// Video options
			const videoElement = document.createElement("video");
			videoElement.preload = "auto";
			videoElement.muted = true;
			videoElement.controls = true;
			videoElement.src = `/videos/${video}`;
			videoElement.loop = true;
			videoElement.autoplay = true;

			// Add event listeners
			videoItem.addEventListener("dblclick", () =>
				showLikeFeedback(video)
			);
			videoItem.addEventListener("wheel", handleScroll);

			// Like feedback
			const likeFeedback = document.createElement("div");
			likeFeedback.classList.add("like-feedback");
			likeFeedback.textContent = "❤️";
			videoItem.appendChild(likeFeedback);

			videoItem.appendChild(videoElement);
			videoContainer.appendChild(videoItem);

			// Observe the video element
			observer.observe(videoElement);
		});
	})
	.catch((error) => {
		console.error("Error fetching videos:", error);
	});

// Like functionality
function showLikeFeedback(video) {
	const videoItem = document.querySelector(
		`.video-item video[src="/videos/${video}"]`
	).parentElement;
	const likeFeedback = videoItem.querySelector(".like-feedback");

	likeFeedback.classList.add("show");
	videoItem.dataset.liked = "true";

	setTimeout(() => {
		likeFeedback.classList.remove("show");
		approve_video(video);
	}, 300);
}

// Scroll functionality
// Rejects the video if it has not been liked
function handleScroll(event) {
	const video = event.currentTarget
		.querySelector("video")
		.src.split("/")
		.pop();

	if (event.deltaY > 0) {
		const videoItem = document.querySelector(
			`.video-item video[src="/videos/${video}"]`
		).parentElement;

		if (!videoItem.dataset.liked) {
			reject_video(video);
		}
	}
}

// Approve functionality
function approve_video(video) {
	// Move the video file to a new directory
	// Post to a specific platform
	fetch(`/videos/${video}`, {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ platform: "PLACEHOLDER" }),
	})
		.then(() => {
			// Refresh the video list
			location.reload(false);
		})
		.catch((error) => {
			console.error("Error moving video:", error);
		});
}

// Reject functionality
function reject_video(video) {
	fetch(`/videos/${video}`, {
		method: "DELETE",
	})
		.then(() => {
			// Refresh the video list
			location.reload(false);
		})
		.catch((error) => {
			console.error("Error removing video:", error);
		});
}
