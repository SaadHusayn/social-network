function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function putRequest(url, requestBody) {
    return fetch(url, {
        method: "PUT",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestBody)
    });
}

async function likeButtonFunctionality(element) {
    const isLikeButton = element.dataset.like === "true" ? 1 : 0;
    try {
        const response = await putRequest('/like', { "like": isLikeButton, "postID": element.dataset.postid });

        if (!response.ok) {
            throw new Error(`Response Status: ${response.status}`);
        }

        // now change the like button content and update like counter
        const postid = element.dataset.postid;
        if (isLikeButton) {
            element.dataset.like = "false";
            element.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-400 group-hover:text-red-600 transition pointer-events-none" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
                </svg>
            `;
            document.querySelector(`.like-count-${postid}`).innerHTML++;
        } else {
            element.dataset.like = "true";
            element.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white group-hover:text-red-600 transition pointer-events-none" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/>
                </svg>
            `;
            document.querySelector(`.like-count-${postid}`).innerHTML--;
        }
    } catch (error) {
        console.error(error.message);
    }
}

function displayEditPostForm(element) {
    const postid = element.dataset.postid;
    const previousPostContent = document.querySelector(`.post-content-${postid}`).innerHTML;
    document.querySelector(`.post-content-${postid}`).innerHTML = `
        <div class="edit-post flex flex-col space-y-2">
            <textarea class="edit-post-content-${postid} w-full px-3 py-2 border border-gray-700 rounded bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-800 transition resize-none" style="min-height: 80px;">${previousPostContent}</textarea>
            <button class="edit-post-submit-button bg-blue-700 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition self-end" data-postid="${postid}">Save</button>
        </div>
    `;
    document.querySelector(`.edit-post-content-${postid}`).focus();
    element.disabled = true;
}

async function editPostSubmitButtonFunctionality(element) {
    const postid = element.dataset.postid;
    const newPostContent = document.querySelector(`.edit-post-content-${postid}`).value;

    try {
        const response = await putRequest('/editPost', { "postContent": newPostContent, "postID": postid });

        if (!response.ok) {
            alert("You cannot edit other user's post!!");
            throw new Error(`Response Status: ${response.status}`);
        }

        document.querySelector(`.post-content-${postid}`).innerHTML = newPostContent;
        document.querySelector(`#edit-post-button-${postid}`).disabled = false;
    } catch (error) {
        console.error(error.message);
    }
}

async function addComment(postID, commentContent) {
    const response = await fetch('/addComment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ "postID": postID, "content": commentContent })
    });

    if (!response.ok) {
        throw new Error(`Response Status: ${response.status}`);
    }

    console.log("Comment added successfully");
}

async function loadComments(postID) {
    //PLACEHOLDER is 11 character string
    userProfileUrl = userProfileUrl.slice(0, -11);

    const response = await fetch(`/getComments?postID=${postID}`);
    if (!response.ok) {
        throw new Error(`Response Status: ${response.status}`);
    }

    const comments = await response.json();
    const commentsContainer = document.querySelector(`#all-the-comments-${postID}`);
    commentsContainer.innerHTML = '';

    if (comments.length === 0) {
        commentsContainer.innerHTML = `
            <div class="bg-gray-800 border border-gray-700 rounded p-4 text-gray-400 text-center">
                No Comments on this post so far.
            </div>
        `;
    } else {
        comments.forEach(comment => {
            // Format date to a pretty format (e.g., "Apr 10, 2024, 2:30 PM")
            let prettyDate = "";
            if (comment.created_at) {
                const date = new Date(comment.created_at.replace(" ", "T"));
                prettyDate = date.toLocaleString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit"
                });
            }
            commentsContainer.innerHTML += `
                <div class="flex items-start space-x-3 bg-gray-800 border border-gray-700 rounded-lg p-4">
                    <img src="${comment.writer.profile_picture ? comment.writer.profile_picture : '/static/network/defaultUserProfilePic.jpg'}"
                        alt="${comment.writer.username}"
                        class="w-10 h-10 rounded-full object-cover border border-gray-600 flex-shrink-0">
                    <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-1">
                            <a href="${userProfileUrl}${comment.writer.username}" class="font-semibold text-blue-400 hover:underline">${comment.writer.username}</a>
                            <span class="text-xs text-gray-400">${prettyDate}</span>
                        </div>
                        <div class="text-gray-200 break-words">${comment.content}</div>
                    </div>
                </div>
            `;
        });
    }

    console.log("comments loaded successfully");
}

document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', async function (event) {
        const element = event.target;
        console.log(element.className);
        if (element.classList.contains("toggle-comment-section-btn")) {
            const postID = element.dataset.postid;
            const section = document.getElementById(`comment-section-${postID}`);
            if (section.classList.contains('hidden')) {
                section.classList.remove('hidden');
                await loadComments(postID);
            } else {
                section.classList.add('hidden');
            }
        } else if (element.classList.contains("like-button")) {
            await likeButtonFunctionality(element);
        } else if (element.classList.contains("edit-post-button")) {
            displayEditPostForm(element);
        } else if (element.classList.contains("edit-post-submit-button")) {
            await editPostSubmitButtonFunctionality(element);
        } else if (element.classList.contains("save-comment-button")) {
            const postID = element.dataset.postid;
            const commentContent = document.querySelector(`#commentContent-${postID}`).value;
            if (commentContent !== "") {
                try {
                    await addComment(postID, commentContent);
                    await loadComments(postID);
                    document.querySelector(`#commentContent-${postID}`).value = "";
                } catch (error) {
                    console.error(error.message);
                }
            }else{
                alert("Comment content is empty.")
            }

        }
    });
});