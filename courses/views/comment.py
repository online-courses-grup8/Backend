from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from courses.serializers import CommentCreateSerializer, CommentSerializer
from courses.selectors import get_course_for_comment
from courses.services import create_course_comment


class CourseCommentCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentCreateSerializer

    def post(self, request, *args, **kwargs):
        course = get_course_for_comment(self.kwargs["slug"])
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        comment = create_course_comment(
            course=course,
            user=request.user,
            validated_data=serializer.validated_data
        )

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )